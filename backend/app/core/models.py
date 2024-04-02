"""
Core models.
"""

import uuid

from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.db import models


class RoomManager(models.Manager):
    """Room manager."""

    def create_room(self, password="", **kwargs):
        "Create, save and return a new room instance."
        room = self.model(**kwargs)
        room.set_password(password)
        room.save(using=self.db)

        return room


class Room(models.Model):
    """Room model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    password = models.CharField(max_length=128, blank=True)

    objects = RoomManager()

    def set_password(self, raw_password):
        """Hash and set password from raw_password."""
        self.password = PBKDF2PasswordHasher().encode(raw_password, uuid.uuid4().hex)

    def check_password(self, raw_password):
        """Return a boolean of whether the raw_password was correct."""
        return PBKDF2PasswordHasher().verify(raw_password, self.password)


class Vote(models.Model):
    """Vote model."""

    VALUE_CHOICES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (5, "5"),
        (8, "8"),
        (13, "13"),
        (20, "20"),
        (40, "40"),
    )

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="votes")
    owner = models.CharField(max_length=20)
    value = models.IntegerField(choices=VALUE_CHOICES, null=True, blank=True)
