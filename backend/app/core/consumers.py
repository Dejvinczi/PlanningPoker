"""
Core consumers.
"""

import json

from asgiref.sync import sync_to_async
from django.db.models import Case, When, Value, BooleanField
from django.core.exceptions import ValidationError
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from core.models import Room, Vote


class PlanningPokerConsumer(AsyncWebsocketConsumer):
    """
    Planning poker game consumer.
    """

    @database_sync_to_async
    def check_room_existing(self):
        """
        Checks if a room exists in the database
        """
        try:
            return Room.objects.filter(id=self.room_id).exists()
        except ValidationError:
            return False

    @database_sync_to_async
    def get_final_vote_list(self):
        """
        Retrieves a list of votes for a room with vote values.
        """
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
        """ "
        Retrieves a list of votes for a room without vote
        values but with information is already voted or not.
        """
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

    @sync_to_async
    def get_vote_choices(self):
        """
        Returns the available vote choices.
        """
        return [{"label": v_c[0], "value": v_c[1]} for v_c in Vote.VALUE_CHOICES]

    @database_sync_to_async
    def update_vote(self, id, value):
        """
        Update voter with specific id vote value.
        """
        vote = Vote.objects.get(id=id)
        vote.value = value
        vote.save()

    @database_sync_to_async
    def reset_vote_values(self):
        """
        Updates all room votes to set value to None.
        """
        Vote.objects.filter(room_id=self.room_id).update(value=None)

    async def connect(self):
        """
        Handles new WebSocket connections, ensuring
        valid room access and initializing state.
        """
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"room_{self.room_id}"

        if not await self.check_room_existing():
            await self.accept()
            await self.message(
                {
                    "code": "error",
                    "message": f"Room does not exist",
                }
            )
            await self.close(code=4001)
            return None

        await self.accept()

        vote_choices = await self.get_vote_choices()
        await self.get_vote_choices_message({"vote_choices": vote_choices})

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.refresh_votes()

    async def disconnect(self, close_code):
        """
        Cleans up on WebSocket disconnection,
        removing the user from the room group.
        """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Handles incoming messages from WebSocket,
        routing actions based on message content.
        """
        text_data_json = json.loads(text_data)
        action = text_data_json["action"]

        match action:
            case "vote":
                await self.vote(text_data_json)
            case "reveal":
                await self.reveal_votes()
            case "reset":
                await self.reset_votes()
            case _:
                await self.message({"code": "error", "message": "Something went wrong"})

    async def vote(self, data):
        """
        Handle vote action from client, updating vote in database
        and refresh votes list in all clients in the room.
        """
        id = data["vote_id"]
        value = data["value"]

        await self.update_vote(id, value)

        await self.message({"code": "success", "message": "Successfully voted."})

        await self.refresh_votes()

    async def refresh_votes(self):
        """Refreshes votes for all clients in the room."""
        votes = await self.get_hidden_vote_list()

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "refresh_votes_message", "votes": votes}
        )

    async def reveal_votes(self):
        """Refreshes votes with revealed values for all clients in the room."""
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
        """
        Updating all votes to value=None and refresh votes for all clients in the room.
        """
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

    async def message(self, event):
        """Handles the message, forwarding it to the client."""
        code = event["code"]
        message = event["message"]

        await self.send(
            text_data=json.dumps(
                {"action": "message", "code": code, "message": message}
            )
        )

    async def get_vote_choices_message(self, event):
        """Handles the get choices message, forwarding it to the client."""
        vote_choices = event["vote_choices"]

        await self.send(
            text_data=json.dumps(
                {"action": "get_vote_choices", "vote_choices": vote_choices}
            )
        )

    async def refresh_votes_message(self, event):
        """Handles the refresh votes message, forwarding it to the client."""
        votes = event["votes"]

        await self.send(
            text_data=json.dumps({"action": "refresh_votes", "votes": votes})
        )

    async def reveal_votes_message(self, event):
        """Handles the reveal votes message, forwarding it to the client."""
        message = event["message"]
        votes = event["votes"]

        await self.send(
            text_data=json.dumps(
                {"action": "reveal_votes", "message": message, "votes": votes}
            )
        )

    async def reset_votes_message(self, event):
        """Handles the reset votes message, forwarding it to the client."""
        message = event["message"]
        votes = event["votes"]

        await self.send(
            text_data=json.dumps(
                {"action": "reset_votes", "message": message, "votes": votes}
            )
        )
