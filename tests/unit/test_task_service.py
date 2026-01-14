"""Unit tests for TaskService."""

import pytest
from src.services.task_service import TaskService


def test_is_empty_returns_true_on_new_service():
    """Test that is_empty() returns True on a newly created service."""
    service = TaskService()
    assert service.is_empty() is True


def test_next_id_starts_at_1():
    """Test that _next_id starts at 1."""
    service = TaskService()
    assert service._next_id == 1


# Tests for add_task()


def test_add_task_creates_task_with_correct_description():
    """Test that add_task creates a task with the correct description."""
    service = TaskService()
    task = service.add_task("Test task")
    assert task.description == "Test task"


def test_add_task_assigns_id_1_on_first_add():
    """Test that the first task is assigned ID 1."""
    service = TaskService()
    task = service.add_task("First task")
    assert task.id == 1


def test_add_task_assigns_id_2_on_second_add():
    """Test that the second task is assigned ID 2."""
    service = TaskService()
    service.add_task("First task")
    task = service.add_task("Second task")
    assert task.id == 2


def test_add_task_makes_is_empty_return_false():
    """Test that is_empty() returns False after adding a task."""
    service = TaskService()
    service.add_task("Test task")
    assert service.is_empty() is False


def test_add_task_raises_valueerror_for_empty_description():
    """Test that add_task raises ValueError for empty description."""
    service = TaskService()
    with pytest.raises(ValueError, match="Task description cannot be empty"):
        service.add_task("")


def test_add_task_raises_valueerror_for_whitespace_only_description():
    """Test that add_task raises ValueError for whitespace-only description."""
    service = TaskService()
    with pytest.raises(ValueError, match="Task description cannot be empty"):
        service.add_task("   ")


def test_add_task_truncates_description_at_200_chars():
    """Test that descriptions longer than 200 characters are truncated."""
    service = TaskService()
    long_description = "a" * 250
    task = service.add_task(long_description)
    assert len(task.description) == 200
    assert task.description == "a" * 200


# Tests for get_all_tasks()


def test_get_all_tasks_returns_empty_list_when_no_tasks():
    """Test that get_all_tasks returns an empty list when no tasks exist."""
    service = TaskService()
    tasks = service.get_all_tasks()
    assert tasks == []


def test_get_all_tasks_returns_all_added_tasks():
    """Test that get_all_tasks returns all tasks that have been added."""
    service = TaskService()
    task1 = service.add_task("Task 1")
    task2 = service.add_task("Task 2")
    tasks = service.get_all_tasks()
    assert len(tasks) == 2
    assert task1 in tasks
    assert task2 in tasks


def test_get_all_tasks_returns_tasks_in_insertion_order():
    """Test that get_all_tasks returns tasks in insertion order."""
    service = TaskService()
    task1 = service.add_task("First")
    task2 = service.add_task("Second")
    task3 = service.add_task("Third")
    tasks = service.get_all_tasks()
    assert tasks[0] == task1
    assert tasks[1] == task2
    assert tasks[2] == task3


# Tests for get_task() and toggle_complete()


def test_get_task_returns_correct_task():
    """Test that get_task returns the correct task by ID."""
    service = TaskService()
    task = service.add_task("Test task")
    retrieved = service.get_task(task.id)
    assert retrieved == task


def test_get_task_raises_keyerror_for_nonexistent_id():
    """Test that get_task raises KeyError for non-existent ID."""
    service = TaskService()
    with pytest.raises(KeyError, match="Task with ID 999 not found"):
        service.get_task(999)


def test_toggle_complete_changes_false_to_true():
    """Test that toggle_complete changes is_complete from False to True."""
    service = TaskService()
    task = service.add_task("Test task")
    assert task.is_complete is False
    service.toggle_complete(task.id)
    assert task.is_complete is True


def test_toggle_complete_changes_true_to_false():
    """Test that toggle_complete changes is_complete from True to False."""
    service = TaskService()
    task = service.add_task("Test task")
    service.toggle_complete(task.id)  # Make it complete
    assert task.is_complete is True
    service.toggle_complete(task.id)  # Toggle back
    assert task.is_complete is False


def test_toggle_complete_raises_keyerror_for_nonexistent_id():
    """Test that toggle_complete raises KeyError for non-existent ID."""
    service = TaskService()
    with pytest.raises(KeyError, match="Task with ID 999 not found"):
        service.toggle_complete(999)


# Tests for update_task()


def test_update_task_updates_description_successfully():
    """Test that update_task updates the task description."""
    service = TaskService()
    task = service.add_task("Original description")
    updated = service.update_task(task.id, "Updated description")
    assert updated.description == "Updated description"
    assert task.description == "Updated description"  # Same object


def test_update_task_raises_keyerror_for_nonexistent_id():
    """Test that update_task raises KeyError for non-existent ID."""
    service = TaskService()
    with pytest.raises(KeyError, match="Task with ID 999 not found"):
        service.update_task(999, "New description")


def test_update_task_raises_valueerror_for_empty_description():
    """Test that update_task raises ValueError for empty description."""
    service = TaskService()
    task = service.add_task("Original")
    with pytest.raises(ValueError, match="Task description cannot be empty"):
        service.update_task(task.id, "")


def test_update_task_truncates_description_at_200_chars():
    """Test that update_task truncates descriptions at 200 characters."""
    service = TaskService()
    task = service.add_task("Original")
    long_description = "b" * 250
    service.update_task(task.id, long_description)
    assert len(task.description) == 200
    assert task.description == "b" * 200


# Tests for delete_task()


def test_delete_task_removes_task_from_storage():
    """Test that delete_task removes the task from storage."""
    service = TaskService()
    task = service.add_task("Test task")
    service.delete_task(task.id)
    with pytest.raises(KeyError):
        service.get_task(task.id)


def test_delete_task_raises_keyerror_for_nonexistent_id():
    """Test that delete_task raises KeyError for non-existent ID."""
    service = TaskService()
    with pytest.raises(KeyError, match="Task with ID 999 not found"):
        service.delete_task(999)


def test_delete_task_id_not_reused_after_deletion():
    """Test that IDs are not reused after deletion."""
    service = TaskService()
    task1 = service.add_task("First task")
    assert task1.id == 1
    service.delete_task(task1.id)
    task2 = service.add_task("Second task")
    assert task2.id == 2  # ID should be 2, not 1
