"""
Core helpers.
"""

import uuid


def generate_room_id():
    # TODO - Delete or save
    """Generate unique based on uuid4 alphanumeric room id."""
    return str(uuid.uuid4()).replace("-", "")
