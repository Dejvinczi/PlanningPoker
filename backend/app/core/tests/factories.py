"""
Core module factories.
"""

import factory

from core.models import (
    Room,
    Vote,
)


class RoomFactory(factory.django.DjangoModelFactory):
    """Room factory."""

    password = factory.PostGenerationMethodCall("set_password", "SamplePassword123")

    class Meta:
        model = Room
        skip_postgeneration_save = True


class VoteFactory(factory.django.DjangoModelFactory):
    """Vote factory."""

    room = factory.SubFactory(RoomFactory)
    owner = factory.Sequence(lambda n: f"SampleOwner{n}")

    class Meta:
        model = Vote
