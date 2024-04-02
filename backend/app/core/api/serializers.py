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

    def create(self, validated_data):
        """Return instance od Vote model."""
        password = validated_data.pop("password", "")
        room_id = validated_data.pop("room")
        voter = validated_data.get("voter")

        # Check if the room exists
        try:
            room = Room.objects.get(id=room_id)
            validated_data.update({"room": room})
        except (Room.DoesNotExist, ValidationError):
            raise serializers.ValidationError({"room": _("Room doesn't exists.")})

        # Check if room password correct
        if not room.check_password(password):
            raise serializers.ValidationError({"password": _("Invalid password.")})

        # Check if the voter already exists in the room
        if Vote.objects.filter(room=room, voter=voter).exists():
            raise serializers.ValidationError(
                {"voter": _("This name is already reserved by another voter.")}
            )

        return super().create(validated_data)
