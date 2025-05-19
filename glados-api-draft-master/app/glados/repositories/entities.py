from glados.models import Entity, Room


def get_entities(filters):
    query = Entity.query

    type = filters.get("type")
    if type:
        query = query.filter(Entity.type == type)

    status = filters.get("status")
    if status:
        query = query.filter(Entity.status == status)

    room = filters.get("room")
    if room:
        query = query.join(Room).filter(Room.name.ilike(room))

    return query


def create_entity(data):
    room_id = data["room_id"]
    if room_id:
        room = Room.query.get_or_404(room_id)
        data["room_id"] = room.id
    entity = Entity(**data)

    return entity


def get_entity_by_id(id):
    entity = Entity.query.get_or_404(id)

    return entity