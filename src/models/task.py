"""Task entity model for the Todo application."""

from dataclasses import dataclass


@dataclass
class Task:
    """Represents a single todo item in the application.

    Attributes:
        id: Unique identifier, auto-generated, starts at 1
        description: Text describing the task, 1-200 characters
        is_complete: Completion status, defaults to False
    """

    id: int
    description: str
    is_complete: bool = False
