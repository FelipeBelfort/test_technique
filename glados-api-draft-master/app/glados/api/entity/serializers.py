from marshmallow import fields, validate

from glados import ma, constants
from glados.models import Entity


class EntitiesBaseSerializer(ma.Schema):
    type = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityType]))
    status = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityStatus]))
    room = fields.String(required=False)
    id = fields.UUID(required=False)
    name = fields.String(required=False, validate=[
        validate.Length(max=25),
        validate.Regexp(r'^[0-9A-Za-zÀ-ÿ\s\-]*$', error="Invalid characters in name")
    ])
    value = fields.String(required=False, allow_none=True)
    room_id = fields.UUID(required=False, allow_none=True)


class EntitiesRequestSerializer(EntitiesBaseSerializer):
    pass


class EntitiesCreateSerializer(EntitiesBaseSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["type"].required = True
        self.fields["status"].required = True
        self.fields["name"].required = True
        self.fields["value"].required = True
        self.fields["room_id"].required = True


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
            "room_id",
        ]


class EntityResponseSerializer(EntitySerializer):
    pass
