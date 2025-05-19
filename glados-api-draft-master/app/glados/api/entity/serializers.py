from marshmallow import fields, validate

from glados import ma, constants
from glados.models import Entity


class EntitiesRequestSerializer(ma.Schema):
    type = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityType]))
    status = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityStatus]))
    room = fields.String(required=False)
    id = fields.UUID(required=False)
    name = fields.String(required=False)
    value = fields.String(required=False, allow_none=True)
    room_id = fields.UUID(required=False, allow_none=True)


class EntitiesCreateSerializer(ma.Schema):
    type = fields.String(required=True, validate=validate.OneOf([x.name for x in constants.EntityType]))
    status = fields.String(required=True, validate=validate.OneOf([x.name for x in constants.EntityStatus]))
    id = fields.UUID(required=False)
    name = fields.String(required=True)
    value = fields.String(required=True, allow_none=True)
    room_id = fields.UUID(required=True, allow_none=True)


class EntitySerializer(ma.Schema):
    created_at = fields.DateTime("%Y-%m-%dT%H:%M:%S")
    room = fields.Function(lambda obj: obj.room.name if obj.room else None)

    class Meta:
        model = Entity
        ordered = True
        fields = [
            "id",
            "name",
            "type",
            "status",
            "value",
            "created_at",
            "room",
        ]


class EntityResponseSerializer(EntitySerializer):
    pass
