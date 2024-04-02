"""
Core views.
"""

from rest_framework import generics

from core.models import Room
from core.api.serializers import CreateRoomSerializer


class CreateRoomAPIView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = CreateRoomSerializer
