"""
Core API tests.
"""

import pytest

from django.urls import reverse
from rest_framework import status

from core.models import Room

CREATE_ROOM_URL = reverse("create-room")


@pytest.mark.django_db
class TestRoomApi:
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
