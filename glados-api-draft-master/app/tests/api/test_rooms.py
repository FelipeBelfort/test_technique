import uuid
import pytest

from glados import constants
from glados.models import Room, Entity


@pytest.fixture
def rooms():
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


def test_get_rooms(client, rooms, mocker):
    response = client.get("/rooms")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "name": "Kitchen",
            "created_at": mocker.ANY,
        },
        {
            "id": "00000000-0000-0000-0000-000000000002",
            "name": "Living Room",
            "created_at": mocker.ANY,
        },
    ]


def test_post_room(client, rooms, mocker):
    response = client.post("/rooms", json={"name": "Bedroom"})

    assert response.status_code == 201
    assert response.json == {
        "id": mocker.ANY,
        "name": "Bedroom",
        "created_at": mocker.ANY,
    }


def test_post_room_with_incomplete_data(client, rooms, mocker):
    response = client.post("/rooms", json={})

    assert response.status_code == 422
    assert response.json == {
        'errors':
        {'name': ['Missing data for required field.']}
    }


def test_post_room_with_invalid_character(client, rooms, mocker):
    response = client.post("/rooms", json={
        "name": "Kitchen2#"}
    )

    assert response.status_code == 422
    assert response.json == {
        'errors':
        {'name': ['Invalid characters in name']}
    }


def test_post_room_with_name_too_long(client, rooms, mocker):
    response = client.post("/rooms", json={
        "name": "abcdefghijklmnopqrstuvxz12"}
    )

    assert response.status_code == 422
    assert response.json == {
        'errors':
        {'name': ['Longer than maximum length 25.']}
    }


def test_patch_room(client, rooms, mocker):
    response = client.patch("/rooms/00000000-0000-0000-0000-000000000001", json={"name": "Kitchen2"})

    assert response.status_code == 200
    assert response.json == {
        "id": "00000000-0000-0000-0000-000000000001",
        "name": "Kitchen2",
        "created_at": mocker.ANY,
    }


def test_patch_room_with_invalid_data(client, rooms, mocker):
    response = client.patch("/rooms/invalid", json={"name": "Kitchen2"})

    assert response.status_code == 422
    assert response.json == {
        'errors':
        {'id': ['Not a valid UUID.']}
    }


def test_patch_room_with_invalid_character(client, rooms, mocker):
    response = client.patch("/rooms/00000000-0000-0000-0000-000000000001", json={
        "name": "Kitchen2#"}
    )

    assert response.status_code == 422
    assert response.json == {
        'errors':
        {'name': ['Invalid characters in name']}
    }


def test_patch_room_with_name_too_long(client, rooms, mocker):
    response = client.patch("/rooms/00000000-0000-0000-0000-000000000001", json={
        "name": "abcdefghijklmnopqrstuvxz12"}
    )

    assert response.status_code == 422
    assert response.json == {
        'errors':
        {'name': ['Longer than maximum length 25.']}
    }


def test_get_entities_from_the_room(client, rooms, mocker):
    response = client.get("/rooms/00000000-0000-0000-0000-000000000001")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "name": "Ceiling Light",
            "type": "light",
            "status": "off",
            "value": None,
            "created_at": mocker.ANY,
            "room": "Kitchen",
            "room_id": "00000000-0000-0000-0000-000000000001",
        }
    ]


def test_get_entities_from_the_room_with_not_found_data(client, rooms, mocker):
    response = client.get("/rooms/00000000-0000-0000-0000-000000000010")

    assert response.status_code == 404
    assert response.json == {
        'message':
        'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'
    }


def test_get_entities_from_the_room_with_invalid_data(client, rooms, mocker):
    response = client.get("/rooms/invalid")

    assert response.status_code == 422
    assert response.json == {
        'errors':
        {'id': ['Not a valid UUID.']}
    }


def test_delete_room(client, rooms, mocker):
    response = client.delete("/rooms/00000000-0000-0000-0000-000000000001")

    assert response.status_code == 204
    get = client.get("/rooms")
    assert all(room["id"] != "00000000-0000-0000-0000-000000000001" for room in get.get_json())


def test_delete_room_with_not_found_data(client, rooms, mocker):
    response = client.delete("/rooms/00000000-0000-0000-0000-000000000010")

    assert response.status_code == 404
    assert response.json == {
        'message':
        'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'
    }


def test_delete_room_with_invalid_data(client, rooms, mocker):
    response = client.delete("/rooms/invalid")

    assert response.status_code == 422
    assert response.json == {
        'errors':
        {'id': ['Not a valid UUID.']}
    }
