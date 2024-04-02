"""
Core API tests.
"""

import pytest

from django.urls import reverse
from rest_framework import status

from core.models import (
    Room,
    Vote,
)

from core.tests.factories import (
    RoomFactory,
    VoteFactory,
)

CREATE_ROOM_URL = reverse("create-room")
JOIN_ROOM_URL = reverse("join-room")


@pytest.mark.django_db
class TestCreateRoomApi:
    """Room API tests."""

    def test_create_room_with_password(self, client):
        """Test create new room with non empty password."""
        payload = {"password": "SamplePassword123"}
        res = client.post(CREATE_ROOM_URL, payload)

        # Check response status and data
        assert res.status_code == status.HTTP_201_CREATED
        assert "id" in res.data
        assert "password" not in res.data

        room = Room.objects.get(id=res.data["id"])

        # Check created room password is blank
        assert room.check_password(payload["password"])

    def test_create_room_with_empty_password(self, client):
        """Test create new room with empty password."""
        payload = {"password": ""}
        res = client.post(CREATE_ROOM_URL, payload)

        # Check response status and data
        assert res.status_code == status.HTTP_201_CREATED
        assert "id" in res.data
        assert "password" not in res.data

        room = Room.objects.get(id=res.data["id"])

        # Check created room password is empty payload password
        assert room.check_password(payload["password"])

    def test_create_room_without_password(self, client):
        """Test create new room without sending password."""
        res = client.post(CREATE_ROOM_URL, {})

        # Check response status and data
        assert res.status_code == status.HTTP_201_CREATED
        assert "id" in res.data
        assert "password" not in res.data

        room = Room.objects.get(id=res.data["id"])

        # Check created room password is blank
        assert room.check_password("")

    def test_create_room_with_too_long_password(self, client):
        """Test create new room error if password is too long."""
        payload = {"password": "SoooooooooTooooooooLoooooooongSamplePassword123"}
        res = client.post(CREATE_ROOM_URL, payload)

        # Check response status and data
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in res.data


@pytest.mark.django_db
class TestJoinRoomApi:
    """Vote API tests."""

    def test_join_existing_room_with_empty_password(self, client):
        """Test join to existing room with empty password."""
        room_password = ""
        room = RoomFactory.create(password=room_password)
        payload = {"room": str(room.id), "password": room_password, "voter": "Voter 1"}
        res = client.post(JOIN_ROOM_URL, payload)

        # Check response status and data
        assert res.status_code == status.HTTP_201_CREATED
        assert "id" in res.data
        assert res.data["id"] == Vote.objects.get(room=room, voter=payload["voter"]).id
        assert "voter" in res.data
        assert res.data["voter"] == payload["voter"]

    def test_join_existing_room_with_non_empty_password(self, client):
        """Test join to existing room with non empty password."""
        room_password = "SamplePassword123"
        room = RoomFactory.create(password=room_password)
        payload = {"room": str(room.id), "password": room_password, "voter": "Voter 1"}
        res = client.post(JOIN_ROOM_URL, payload)

        # Check response status and data
        assert res.status_code == status.HTTP_201_CREATED
        assert "id" in res.data
        assert res.data["id"] == Vote.objects.get(room=room, voter=payload["voter"]).id
        assert "voter" in res.data
        assert res.data["voter"] == payload["voter"]

    def test_join_non_existing_room(self, client):
        """Test join to non existing room."""
        payload = {
            "room": "NoExistingRoomId",
            "password": "NoExistingRoomPassword",
            "voter": "Voter 1",
        }
        res = client.post(JOIN_ROOM_URL, payload)

        # Check response status and data
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert "id" not in res.data
        assert "room" in res.data

    def test_join_existing_room_with_existing_voter(self, client):
        """Test join to existing room with already existed voter name."""
        raw_password = ""
        room = RoomFactory.create(password=raw_password)
        vote = VoteFactory(room=room, voter="Voter1")
        payload = {"room": str(room.id), "password": raw_password, "voter": vote.voter}
        res = client.post(JOIN_ROOM_URL, payload)

        # Check response status and data
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert "id" not in res.data
        assert "voter" in res.data
