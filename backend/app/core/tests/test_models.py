"""
Core models tests.
"""

import pytest

from core.models import Room


@pytest.mark.django_db
class TestRoom:
    """Room model tests."""

    def test_create_room_without_password(self):
        """Test creating room without password."""
        room = Room.objects.create_room()

        assert Room.objects.all().count() == 1
        assert room.check_password("")

    def test_create_room_with_password(self):
        """Test creating room with password."""
        password = "SamplePassword123"
        room = Room.objects.create_room(password=password)

        assert Room.objects.all().count() == 1
        assert room.check_password(password)
