"""
Core helpers.
"""

import uuid


def generate_room_link():
    # TODO - Delete or save
    """Generate unique based on uuid4 alphanumeric room link."""
    return str(uuid.uuid4()).replace("-", "")
