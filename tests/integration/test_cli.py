"""Integration tests for CLI workflows."""

from unittest.mock import Mock, patch
from rich.console import Console
from src.services.task_service import TaskService
from src.cli.menu import (
    handle_add_task,
    handle_view_tasks,
    handle_update_task,
    handle_delete_task,
    handle_toggle_complete,
)


def test_add_task_workflow():
    """Test complete add task workflow."""
    console = Mock(spec=Console)
    service = TaskService()

    # Mock user input
    with patch('src.cli.menu.get_description', return_value="Buy groceries"):
        handle_add_task(console, service)

    # Verify task was created
    tasks = service.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].description == "Buy groceries"

    # Verify success message was printed
    console.print.assert_called_once()
    assert "created successfully" in str(console.print.call_args)


def test_view_tasks_workflow_empty_list():
    """Test viewing tasks when list is empty."""
    console = Mock(spec=Console)
    service = TaskService()

    handle_view_tasks(console, service)

    # Verify "No tasks found" message
    console.print.assert_called_once()
    assert "No tasks found" in str(console.print.call_args)


def test_view_tasks_workflow_with_tasks():
    """Test viewing tasks when tasks exist."""
    console = Mock(spec=Console)
    service = TaskService()

    # Add tasks
    service.add_task("Task 1")
    service.add_task("Task 2")

    handle_view_tasks(console, service)

    # Verify table was printed
    console.print.assert_called_once()


def test_complete_workflow_add_view_mark_complete_delete():
    """Test complete workflow: Add → View → Mark Complete → Delete → Exit."""
    console = Mock(spec=Console)
    service = TaskService()

    # Step 1: Add task
    with patch('src.cli.menu.get_description', return_value="Test task"):
        handle_add_task(console, service)

    tasks = service.get_all_tasks()
    assert len(tasks) == 1
    task_id = tasks[0].id

    # Step 2: View tasks
    console.print.reset_mock()
    handle_view_tasks(console, service)
    console.print.assert_called_once()

    # Step 3: Mark complete
    console.print.reset_mock()
    with patch('src.cli.menu.get_task_id', return_value=task_id):
        handle_toggle_complete(console, service)

    task = service.get_task(task_id)
    assert task.is_complete is True
    assert "marked as complete" in str(console.print.call_args)

    # Step 4: Delete task
    console.print.reset_mock()
    with patch('src.cli.menu.get_task_id', return_value=task_id):
        handle_delete_task(console, service)

    tasks = service.get_all_tasks()
    assert len(tasks) == 0
    assert "deleted successfully" in str(console.print.call_args)


def test_error_handling_empty_description():
    """Test error handling for empty description."""
    console = Mock(spec=Console)
    service = TaskService()

    # Try to add task with empty description
    with patch('src.cli.menu.get_description', return_value=""):
        handle_add_task(console, service)

    # Verify error message was printed
    console.print.assert_called_once()
    assert "Error" in str(console.print.call_args)

    # Verify no task was created
    assert service.is_empty()


def test_error_handling_nonexistent_id():
    """Test error handling for non-existent task ID."""
    console = Mock(spec=Console)
    service = TaskService()

    # Add a task first so we're not in empty state
    service.add_task("Existing task")

    # Try to update non-existent task
    with patch('src.cli.menu.get_task_id', return_value=999), \
         patch('src.cli.menu.get_description', return_value="New description"):
        handle_update_task(console, service)

    # Verify error message was printed
    console.print.assert_called()
    print_calls = [str(call) for call in console.print.call_args_list]
    assert any("not found" in call for call in print_calls)


def test_error_handling_operations_on_empty_list():
    """Test error handling when operations are attempted on empty list."""
    console = Mock(spec=Console)
    service = TaskService()

    # Try to update when no tasks exist
    handle_update_task(console, service)
    assert "No tasks to update" in str(console.print.call_args)

    # Try to delete when no tasks exist
    console.print.reset_mock()
    handle_delete_task(console, service)
    assert "No tasks to delete" in str(console.print.call_args)

    # Try to toggle complete when no tasks exist
    console.print.reset_mock()
    handle_toggle_complete(console, service)
    assert "No tasks to update" in str(console.print.call_args)
