from flask import request
from flask_restful import Resource

from glados.api.entity.serializers import EntitiesRequestSerializer, EntityResponseSerializer, EntitiesCreateSerializer
from glados.repositories.entities import get_entities, create_entity, get_entity_by_id
from glados import db


class EntitiesAPI(Resource):
    def get(self):
        request_serializer = EntitiesRequestSerializer()
        data = request_serializer.load(request.args)

        entities = get_entities(data)

        serializer = EntityResponseSerializer(many=True)
        return serializer.dump(entities), 200

    def post(self):
        request_serializer = EntitiesCreateSerializer()
        data = request_serializer.load(request.get_json())
        entity = create_entity(data)
        db.session.add(entity)
        db.session.commit()

        serializer = EntityResponseSerializer()
        return serializer.dump(entity), 201


class EntitiesDetailsAPI(Resource):
    request_serializer = EntitiesRequestSerializer()

    def patch(self, id):
        self.request_serializer.load({"id": id})
        data = self.request_serializer.load(request.get_json())
        entity = get_entity_by_id(id)
        modified = False
        for k, v in data.items():
            if getattr(entity, k) != v:
                setattr(entity, k, v)
                modified = True
        if modified:
            db.session.commit()
        serializer = EntityResponseSerializer()

        return serializer.dump(entity), 200

    def delete(self, id):
        self.request_serializer.load({"id": id})
        entity = get_entity_by_id(id)
        db.session.delete(entity)
        db.session.commit()

        return "", 204
