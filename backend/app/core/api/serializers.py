"""Core serializers."""

from rest_framework import serializers

from .. import models


class CreateRoomSerializer(serializers.ModelSerializer):
    """Room model serializer."""

    password = serializers.CharField(max_length=30, write_only=True, required=False)

    def create(self, validated_data):
        return models.Room.objects.create_room(**validated_data)

    class Meta:
        model = models.Room
        fields = [
            "id",
            "password",
        ]
        read_only = ["id"]
