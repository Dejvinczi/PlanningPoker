"""
Core urls.
"""

from django.urls import path

from core.api import views

urlpatterns = [
    path("create-room", views.CreateRoomAPIView.as_view(), name="create-room"),
    path("join-room", views.JoinRoomAPIView.as_view(), name="join-room"),
]
