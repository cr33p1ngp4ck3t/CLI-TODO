"""CLI menu display and user input handling."""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.table import Table

try:
    import pyfiglet
    PYFIGLET_AVAILABLE = True
except ImportError:
    PYFIGLET_AVAILABLE = False


def create_ascii_header() -> str:
    """Generate ASCII art title for the application.

    Returns:
        ASCII art string for "CLI TODO" or plain text fallback
    """
    if PYFIGLET_AVAILABLE:
        return pyfiglet.figlet_format("CLI TODO")
    else:
        return "CLI TODO"


def display_menu(console: Console) -> None:
    """Display the main menu with styled Rich components.

    Args:
        console: Rich Console instance for styled output
    """
    # Display ASCII art header
    header = create_ascii_header()
    console.print(header, style="bold cyan")

    # Create menu table
    table = Table(title="[bold blue_violet]Main Menu", show_header=False, padding=(0, 2))
    table.add_column("Option", style="bold grey0")
    table.add_column("Description", style="white")

    table.add_row("1", "Add Task")
    table.add_row("2", "Update Task")
    table.add_row("3", "Delete Task")
    table.add_row("4", "Mark Complete/Incomplete")
    table.add_row("5", "Exit")

    # Display menu in a panel
    # menu_panel = Panel(
    #     table,
    #     # title="[bold blue_violet]Main Menu",
    # )
    console.print(table)


def get_user_choice(console: Console) -> str:
    """Prompt user for menu choice with Rich styling.

    Args:
        console: Rich Console instance for styled output

    Returns:
        User's menu choice as a string
    """
    choice = Prompt.ask(
        "[bold yellow]> ",
        choices=["1", "2", "3", "4", "5"],
        show_choices=False
    )
    return choice


def get_task_id(console: Console) -> int:
    """Prompt user for task ID with validation.

    Args:
        console: Rich Console instance for styled output

    Returns:
        Valid task ID as integer
    """
    task_id = IntPrompt.ask("[bold yellow]Enter task ID[/bold yellow]")
    return task_id


def get_description(console: Console, prompt_text: str = "Enter task description") -> str:
    """Prompt user for task description.

    Args:
        console: Rich Console instance for styled output
        prompt_text: Custom prompt text (default: "Enter task description")

    Returns:
        User input as string
    """
    description = Prompt.ask(f"[bold yellow]{prompt_text}[/bold yellow]")
    return description


# Action Handlers


def handle_add_task(console: Console, task_service) -> None:
    """Handle adding a new task.

    Args:
        console: Rich Console instance for styled output
        task_service: TaskService instance
    """
    description = get_description(console)
    try:
        task = task_service.add_task(description)
        console.print(f"[bold green]✓ Task {task.id} created successfully[/bold green]")
    except ValueError as e:
        console.print(f"[bold red]✗ Error: {e}[/bold red]")


def handle_view_tasks(console: Console, task_service) -> None:
    """Handle viewing all tasks.

    Args:
        console: Rich Console instance for styled output
        task_service: TaskService instance
    """
    tasks = task_service.get_all_tasks()

    if not tasks:
        console.print("[red]No tasks found. Add a task to get started![/red]")
        return

    # Create tasks table
    table = Table(title="[bold blue_violet]Your Tasks[/bold blue_violet]", show_header=True, header_style="bold blue_violet" )
    table.add_column("Status", style="bold", width=8)
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Description", style="white")

    for task in tasks:
        status = "[green]✓[/green]" if task.is_complete else "[yellow]○[/yellow]"
        row_style = "green" if task.is_complete else "white"
        table.add_row(status, str(task.id), task.description, style=row_style)

    console.print(table)


def handle_update_task(console: Console, task_service) -> None:
    """Handle updating a task description.

    Args:
        console: Rich Console instance for styled output
        task_service: TaskService instance
    """
    if task_service.is_empty():
        console.print("[yellow]⚠ No tasks to update. Add a task first![/yellow]")
        return

    task_id = get_task_id(console)
    new_description = get_description(console, "Enter new description")

    try:
        task = task_service.update_task(task_id, new_description)
        console.print(f"[bold green]✓ Task {task.id} updated successfully[/bold green]")
    except KeyError as e:
        console.print(f"[bold red]✗ {e}[/bold red]")
    except ValueError as e:
        console.print(f"[bold red]✗ Error: {e}[/bold red]")


def handle_delete_task(console: Console, task_service) -> None:
    """Handle deleting a task.

    Args:
        console: Rich Console instance for styled output
        task_service: TaskService instance
    """
    if task_service.is_empty():
        console.print("[yellow]⚠ No tasks to delete. Add a task first![/yellow]")
        return

    task_id = get_task_id(console)

    try:
        task_service.delete_task(task_id)
        console.print(f"[bold green]✓ Task {task_id} deleted successfully[/bold green]")
    except KeyError as e:
        console.print(f"[bold red]✗ {e}[/bold red]")


def handle_toggle_complete(console: Console, task_service) -> None:
    """Handle toggling task completion status.

    Args:
        console: Rich Console instance for styled output
        task_service: TaskService instance
    """
    if task_service.is_empty():
        console.print("[yellow]⚠ No tasks to update. Add a task first![/yellow]")
        return

    task_id = get_task_id(console)

    try:
        task = task_service.toggle_complete(task_id)
        status_text = "complete" if task.is_complete else "incomplete"
        console.print(f"[bold green]✓ Task {task.id} marked as {status_text}[/bold green]")
    except KeyError as e:
        console.print(f"[bold red]✗ {e}[/bold red]")
