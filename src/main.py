"""Main entry point for the Todo application."""

from rich.console import Console # pyright: ignore[reportMissingImports]
from rich.panel import Panel # type: ignore
from rich.table import Table

from src.services.task_service import TaskService
from src.cli.menu import (
    display_menu,
    get_user_choice,
    handle_add_task,
    handle_view_tasks,
    handle_update_task,
    handle_delete_task,
    handle_toggle_complete,
)


def main() -> None:
    """Run the Todo application main loop."""
    console = Console()
    task_service = TaskService()

    while True:
        # Clear screen and display menu
        console.clear()
        display_menu(console)
        handle_view_tasks(console, task_service)
        
        # Get user choice
        choice = get_user_choice(console)

        # Dispatch to appropriate handler
        if choice == "1":
            handle_add_task(console, task_service)
        elif choice == "2":
            handle_update_task(console, task_service)
        elif choice == "3":
            handle_delete_task(console, task_service)
        elif choice == "4":
            handle_toggle_complete(console, task_service)
        elif choice == "5":
            # Display goodbye message and exit
            console.print("\n[bold white]👋 Goodbye![/bold white]\n")
            break
        else:
            console.print("[yellow]⚠ Invalid option. Please try again.[/yellow]")

        # Wait for user to press Enter before continuing
        console.input("\n[dim]Press Enter to continue...[/dim]")


if __name__ == "__main__":
    main()
