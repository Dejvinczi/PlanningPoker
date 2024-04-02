"""
Core routing.
"""

from django.urls import path
from core.consumers import (
    PlanningPokerConsumer,
)

websocket_urlpatterns = [
    path("ws/room/<str:room_id>", PlanningPokerConsumer.as_asgi()),
]
