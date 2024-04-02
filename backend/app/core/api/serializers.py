"""
Core serializers.
"""

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from rest_framework import serializers

from core.models import (
    Room,
    Vote,
)


class CreateRoomSerializer(serializers.ModelSerializer):
    """Room model serializer."""

    class Meta:
        model = Room
        fields = ["id", "password"]
        read_only = ["id"]
        extra_kwargs = {"password": {"write_only": True, "max_length": 30}}

    def create(self, validated_data):
        """Return instance od Room model."""
        return Room.objects.create_room(**validated_data)


class JoinRoomSerializer(serializers.ModelSerializer):
    """Vote model serializer."""

    room = serializers.CharField(allow_blank=False, write_only=True, required=True)
    password = serializers.CharField(
        max_length=30, write_only=True, allow_blank=True, required=True
    )

    class Meta:
        model = Vote
        fields = ["id", "room", "password", "voter"]
        read_only = ["id"]

    def validate_room(self, value):
        """Validate if the room exists."""
        try:
            return Room.objects.get(id=value)
        except (Room.DoesNotExist, ValidationError):
            raise serializers.ValidationError({"room": _("Room doesn't exists.")})

    def validate(self, data):
        """Object level validation."""
        room = data.get("room")
        password = data.pop("password", "")
        voter = data.get("voter")

        if not room.check_password(password):
            raise serializers.ValidationError({"password": _("Invalid password.")})

        if Vote.objects.filter(room=room, voter=voter).exists():
            raise serializers.ValidationError(
                {"voter": _("This name is already reserved by another voter.")}
            )

        return data
