"""
Core consumers.
"""

import json
from django.db.models import Case, When, Value, BooleanField
from django.core.exceptions import ValidationError
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Room, Vote


class PlanningPokerConsumer(AsyncWebsocketConsumer):
    """Planning poker game consumer."""

    @database_sync_to_async
    def check_room_existing(self):
        try:
            return Room.objects.filter(id=self.room_id).exists()
        except (Room.DoesNotExist, ValidationError):
            return False

    @database_sync_to_async
    def get_final_vote_list(self):
        votes = (
            Vote.objects.filter(room_id=self.room_id)
            .annotate(
                voted=Case(
                    When(value__isnull=True, then=Value(False)),
                    default=Value(True),
                    output_field=BooleanField(),
                )
            )
            .values("voter", "value", "voted")
        )
        return list(votes)

    @database_sync_to_async
    def get_hidden_vote_list(self):
        votes = (
            Vote.objects.filter(room_id=self.room_id)
            .annotate(
                voted=Case(
                    When(value__isnull=True, then=Value(False)),
                    default=Value(True),
                    output_field=BooleanField(),
                )
            )
            .values("voter", "voted")
        )
        return list(votes)

    @database_sync_to_async
    def get_vote_choices(self):
        return [{"label": v_c[0], "value": v_c[1]} for v_c in Vote.VALUE_CHOICES]

    @database_sync_to_async
    def update_vote(self, id, value):
        vote = Vote.objects.get(id=id)
        vote.value = value
        vote.save()

    @database_sync_to_async
    def reset_vote_values(self):
        Vote.objects.filter(room_id=self.room_id).update(value=None)

    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"room_{self.room_id}"

        if not await self.check_room_existing():
            await self.accept()
            await self.send(
                text_data=json.dumps(
                    {"error": f"Room with ID {self.room_id} does not exist."}
                )
            )
            await self.close(code=4001)
            return None

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        vote_choices = await self.get_vote_choices()
        await self.send(
            text_data=json.dumps(
                {"action": "refresh_vote_choices", "vote_choices": vote_choices}
            )
        )

        await self.refresh_votes()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json["action"]

        if action == "vote":
            await self.vote(text_data_json)
        elif action == "reveal":
            await self.reveal_votes()
        elif action == "reset":
            await self.reset_votes()

    async def refresh_vote_choices(self):
        vote_choices = await self.get_vote_choices()

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "refresh_vote_choices_message", "vote_choices": vote_choices},
        )

    async def vote(self, data):
        id = data["vote_id"]
        value = data["value"]
        await self.update_vote(id, value)

        await self.refresh_votes()

    async def refresh_votes(self):
        votes = await self.get_hidden_vote_list()

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "refresh_votes_message", "votes": votes}
        )

    async def reveal_votes(self):
        votes = await self.get_final_vote_list()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "reveal_votes_message",
                "message": "Votes have been revealed.",
                "votes": votes,
            },
        )

    async def reset_votes(self):
        await self.reset_vote_values()
        votes_list = await self.get_hidden_vote_list()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "reset_votes_message",
                "message": "Votes have been reset.",
                "votes": votes_list,
            },
        )

    async def refresh_votes_message(self, event):
        votes = event["votes"]

        await self.send(
            text_data=json.dumps({"action": "refresh_votes", "votes": votes})
        )

    async def reveal_votes_message(self, event):
        message = event["message"]
        votes = event["votes"]

        await self.send(
            text_data=json.dumps(
                {"action": "reveal_votes", "message": message, "votes": votes}
            )
        )

    async def reset_votes_message(self, event):
        message = event["message"]
        votes = event["votes"]

        await self.send(
            text_data=json.dumps(
                {"action": "reset_votes", "message": message, "votes": votes}
            )
        )
