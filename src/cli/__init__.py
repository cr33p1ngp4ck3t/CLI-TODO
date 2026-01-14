"""CLI interface components package."""

from src.cli.menu import (
    create_ascii_header,
    display_menu,
    get_user_choice,
    get_task_id,
    get_description,
    handle_add_task,
    handle_view_tasks,
    handle_update_task,
    handle_delete_task,
    handle_toggle_complete,
)

__all__ = [
    "create_ascii_header",
    "display_menu",
    "get_user_choice",
    "get_task_id",
    "get_description",
    "handle_add_task",
    "handle_view_tasks",
    "handle_update_task",
    "handle_delete_task",
    "handle_toggle_complete",
]
