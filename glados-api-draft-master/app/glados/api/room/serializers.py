from marshmallow import fields

from glados import ma
from glados.models import Room


class RoomsRequestSerializer(ma.Schema):
    name = fields.String(required=False)
    id = fields.UUID(required=False)


class RoomsCreationSerializer(ma.Schema):
    name = fields.String(required=True)


class RoomSerializer(ma.Schema):
    created_at = fields.DateTime("%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Room
        ordered = True
        fields = [
            "id",
            "name",
            "created_at",
        ]


class RoomResponseSerializer(RoomSerializer):
    pass
