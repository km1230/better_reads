"""Choices for choiceField based on Enum."""
from enum import Enum


class ReadStatus(Enum):
    """Read status for books."""

    wish = "wish"
    reading = "reading"
    read = "read"

    @staticmethod
    def choices():
        """Options for Django dropdowns."""
        return (
            (ReadStatus.wish.value, "wish"),
            (ReadStatus.reading.value, "reading"),
            (ReadStatus.read.value, "read"),
        )
