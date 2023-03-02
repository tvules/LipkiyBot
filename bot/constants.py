from enum import Enum


class CommonMessage(str, Enum):
    """Common messages used to respond to the user."""

    GREETING = "👋🏻"
