from marshmallow import fields, validate

from glados import ma
from glados.models import Room


class RoomsRequestSerializer(ma.Schema):
    name = fields.String(required=False, validate=[
        validate.Length(max=25),
        validate.Regexp(r'^[0-9A-Za-zÀ-ÿ\s\-]*$', error="Invalid characters in name")
    ])
    id = fields.UUID(required=False)


class RoomsCreationSerializer(ma.Schema):
    name = fields.String(required=True, validate=[
        validate.Length(max=25),
        validate.Regexp(r'^[0-9A-Za-zÀ-ÿ\s\-]*$', error="Invalid characters in name")
    ])


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
