from glados.models import Room


def get_rooms():
    query = Room.query

    return query


def get_room_by_id(id):
    query = Room.query.get_or_404(id)

    return query


def create_room(data):
    room = Room(**data)

    return room
