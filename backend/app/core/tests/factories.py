"""
Core module factories.
"""

import factory

from core.models import Room


class RoomFactory(factory.django.DjangoModelFactory):
    """Room factory."""

    password = factory.PostGenerationMethodCall("set_password", "SamplePassword123")

    class Meta:
        model = Room
        skip_postgeneration_save = True
