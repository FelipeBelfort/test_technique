from flask import request
from flask_restful import Resource
from glados import db

from glados.api.room.serializers import RoomResponseSerializer, RoomsRequestSerializer
from glados.api.entity.serializers import EntityResponseSerializer
from glados.repositories.rooms import get_rooms, get_room_by_id, create_room


class RoomsAPI(Resource):
    def get(self):
        rooms = get_rooms()

        serializer = RoomResponseSerializer(many=True)
        return serializer.dump(rooms), 200

    def post(self):
        serializer = RoomResponseSerializer()
        request_serializer = RoomsRequestSerializer()

        room_data = request_serializer.load(request.get_json())
        room = create_room(room_data)
        db.session.add(room)
        db.session.commit()

        return serializer.dump(room), 201


class RoomsDetailsAPI(Resource):
    request_serializer = RoomsRequestSerializer()

    def patch(self, id):
        data = request.get_json()
        data = self.request_serializer.load({**data, "id": id})
        room = get_room_by_id(data["id"])
        if "name" in data:
            room.name = data["name"]
            db.session.commit()
        serializer = RoomResponseSerializer()

        return serializer.dump(room), 200

    def delete(self, id):
        data = self.request_serializer.load({"id": id})
        room = get_room_by_id(data["id"])
        db.session.delete(room)
        db.session.commit()

        return "", 204

    def get(self, id):
        data = self.request_serializer.load({"id": id})
        room = get_room_by_id(data["id"])
        serializer = EntityResponseSerializer(many=True)

        return serializer.dump(room.entities), 200
