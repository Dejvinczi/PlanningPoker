"""
Core urls.
"""

from django.urls import path
from .api import views


urlpatterns = [
    path("", views.CreateRoomAPIView.as_view(), name="create-room"),
]
