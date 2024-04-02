"""
Core serializers.
"""

from rest_framework import serializers

from core.models import Room


class CreateRoomSerializer(serializers.ModelSerializer):
    """Creation room model serializer."""

    password = serializers.CharField(max_length=30, write_only=True, required=False)

    def create(self, validated_data):
        """Return instance od Room model."""
        return Room.objects.create_room(**validated_data)

    class Meta:
        model = Room
        fields = [
            "id",
            "password",
        ]
        read_only = ["id"]
