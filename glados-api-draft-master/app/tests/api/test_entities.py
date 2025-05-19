import uuid
import pytest

from glados import constants
from glados.models import Entity, Room


@pytest.fixture
def entities():
    kitchen = Room(id=uuid.UUID(int=1), name="Kitchen")
    kitchen.save(commit=False)

    living_room = Room(id=uuid.UUID(int=2), name="Living Room")
    living_room.save(commit=False)

    entity = Entity(
        id=uuid.UUID(int=1),
        name="Ceiling Light",
        type=constants.EntityType.light.name,
        status=constants.EntityStatus.off.name,
        value=None,
        room_id=kitchen.id)
    entity.save(commit=False)

    entity = Entity(
        id=uuid.UUID(int=2),
        name="Lamp",
        type=constants.EntityType.light.name,
        status=constants.EntityStatus.on.name,
        value=200,
        room_id=living_room.id)
    entity.save(commit=False)

    entity = Entity(
        id=uuid.UUID(int=3),
        name="Thermometer",
        type=constants.EntityType.sensor.name,
        status=constants.EntityStatus.on.name,
        value=28,
        room_id=living_room.id)
    entity.save(commit=False)


def test_get_entities_with_invalid_type_data(client):
    response = client.get("/entities?type=invalid")

    assert response.status_code == 422
    assert response.json == {"errors": {
        "type": ["Must be one of: sensor, light, switch, multimedia, air_conditioner."]
    }}


def test_get_entities_with_invalid_status_data(client):
    response = client.get("/entities?status=invalid")

    assert response.status_code == 422
    assert response.json == {"errors": {
        "status": ["Must be one of: on, off, unavailable."]
    }}


def test_get_entities_with_invalid_room_data(client):
    response = client.get("/entities?room=invalid")

    assert response.status_code == 200
    assert response.json == []


def test_get_entities(client, entities, mocker):
    response = client.get("/entities")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "name": "Ceiling Light",
            "type": "light",
            "status": "off",
            "value": None,
            "created_at": mocker.ANY,
            "room": "Kitchen"
        },
        {
            "id": "00000000-0000-0000-0000-000000000002",
            "name": "Lamp",
            "type": "light",
            "status": "on",
            "value": "200",
            "created_at": mocker.ANY,
            "room": "Living Room"
        },
        {
            "id": "00000000-0000-0000-0000-000000000003",
            "name": "Thermometer",
            "type": "sensor",
            "status": "on",
            "value": "28",
            "created_at": mocker.ANY,
            "room": "Living Room"
        }
    ]


def test_get_entities_with_type_filter(client, entities, mocker):
    response = client.get("/entities?type=sensor")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000003",
            "name": "Thermometer",
            "type": "sensor",
            "status": "on",
            "value": "28",
            "created_at": mocker.ANY,
            "room": "Living Room"
        }
    ]


def test_get_entities_with_status_filter(client, entities, mocker):
    response = client.get("/entities?status=on")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000002",
            "name": "Lamp",
            "type": "light",
            "status": "on",
            "value": "200",
            "created_at": mocker.ANY,
            "room": "Living Room"
        },
        {
            "id": "00000000-0000-0000-0000-000000000003",
            "name": "Thermometer",
            "type": "sensor",
            "status": "on",
            "value": "28",
            "created_at": mocker.ANY,
            "room": "Living Room"
        }
    ]


def test_get_entities_with_room_filter(client, entities, mocker):
    response = client.get("/entities?room=Kitchen")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "name": "Ceiling Light",
            "type": "light",
            "status": "off",
            "value": None,
            "created_at": mocker.ANY,
            "room": "Kitchen"
        }
    ]


def test_get_entities_with_multiple_filters(client, entities, mocker):
    response = client.get("/entities?status=on&type=light")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000002",
            "name": "Lamp",
            "type": "light",
            "status": "on",
            "value": "200",
            "created_at": mocker.ANY,
            "room": "Living Room"
        },
    ]


def test_post_entity(client, entities, mocker):
    response = client.post("/entities", json={
        "name": "Kitchen light",
        "type": constants.EntityType.light.name,
        "status": constants.EntityStatus.off.name,
        "value": None,
        "room_id": "00000000-0000-0000-0000-000000000001",
    })

    assert response.status_code == 201
    assert response.json == {
        "id": mocker.ANY,
        "name": "Kitchen light",
        "type": "light",
        "status": "off",
        "value": None,
        "created_at": mocker.ANY,
        "room": "Kitchen"
    }


def test_post_entity_with_incomplete_data(client, entities, mocker):
    response = client.post("/entities", json={
        "name": "Kitchen light",
        "value": None,
        "room_id": "00000000-0000-0000-0000-000000000001",
    })

    assert response.status_code == 422
    assert response.json == {
        'errors': {
            'status': ['Missing data for required field.'], 
            'type': ['Missing data for required field.']
        }
    }


def test_post_entity_with_not_found_room(client, entities, mocker):
    response = client.post("/entities", json={
        "name": "Kitchen light",
        "type": constants.EntityType.light.name,
        "status": constants.EntityStatus.off.name,
        "value": None,
        "room_id": "00000000-0000-0000-0000-000000000010",
    })

    assert response.status_code == 404
    assert response.json == {
        'message':
        'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'
    }


def test_patch_entity(client, entities, mocker):
    response = client.patch("/entities/00000000-0000-0000-0000-000000000001", json={
        "status": "on",
        "name": "new name"
    })

    print(response.json)
    assert response.status_code == 200
    assert response.json == {
        "id": "00000000-0000-0000-0000-000000000001",
        "name": "new name",
        "type": "light",
        "status": "on",
        "value": None,
        "created_at": mocker.ANY,
        "room": "Kitchen"
    }


def test_patch_entity_with_invalid_id(client, entities, mocker):
    response = client.patch("/entities/invalid", json={"name": "New name"})

    assert response.status_code == 422
    assert response.json == {
        'errors':
        {'id': ['Not a valid UUID.']}
    }


def test_patch_entity_with_invalid_data(client, entities, mocker):
    response = client.patch("/entities/00000000-0000-0000-0000-000000000001", json={"type": "invalid"})

    assert response.status_code == 422
    assert response.json == {"errors": {
        "type": ["Must be one of: sensor, light, switch, multimedia, air_conditioner."]
    }}


def test_patch_entity_with_not_found_data(client, entities, mocker):
    response = client.patch("/entities/00000000-0000-0000-0000-000000000010", json={"name": "New name"})

    assert response.status_code == 404
    assert response.json == {
        'message':
        'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'
    }


def test_delete_entity(client, entities, mocker):
    response = client.delete("/entities/00000000-0000-0000-0000-000000000001")

    assert response.status_code == 204
    get = client.get("/entities")
    assert all(entity["id"] != "00000000-0000-0000-0000-000000000001" for entity in get.get_json())


def test_delete_entity_with_not_found_data(client, entities, mocker):
    response = client.delete("/entities/00000000-0000-0000-0000-000000000010")

    assert response.status_code == 404
    assert response.json == {
        'message':
        'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'
    }


def test_delete_entity_with_invalid_data(client, entities, mocker):
    response = client.delete("/entities/invalid")

    assert response.status_code == 422
    assert response.json == {
        'errors':
        {'id': ['Not a valid UUID.']}
    }
