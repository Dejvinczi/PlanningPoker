"""
Core models tests.
"""

import pytest

from core.models import (
    Room,
    Vote,
)
from core.tests.factories import (
    RoomFactory,
    VoteFactory,
)


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


@pytest.mark.django_db
class TestVote:
    """Vote model tests."""

    def test_create_vote(self):
        """Test creating vote."""
        room = RoomFactory.create()
        owner = "SampleOwner"
        vote = Vote.objects.create(room=room, owner=owner)

        assert Vote.objects.all().count() == 1
        assert vote.owner == owner
        assert vote.room.id == room.id
        assert vote.value is None

    def test_update_vote(self):
        """Test update vote."""
        vote = VoteFactory.create()
        new_vote_value = 1
        vote.value = new_vote_value
        vote.save()

        assert vote.value == new_vote_value
