"""
Core views.
"""

from rest_framework import generics

from core.api.serializers import (
    CreateRoomSerializer,
    JoinRoomSerializer,
)


class CreateRoomAPIView(generics.CreateAPIView):
    """Create new room API view."""

    serializer_class = CreateRoomSerializer


class JoinRoomAPIView(generics.CreateAPIView):
    """Join existing room API view."""

    serializer_class = JoinRoomSerializer
