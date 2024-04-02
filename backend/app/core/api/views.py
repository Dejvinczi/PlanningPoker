"""
Core views.
"""

from rest_framework import (
    generics,
)

from .. import models
from . import serializers


class CreateRoomAPIView(generics.CreateAPIView):
    queryset = models.Room.objects.all()
    serializer_class = serializers.CreateRoomSerializer
