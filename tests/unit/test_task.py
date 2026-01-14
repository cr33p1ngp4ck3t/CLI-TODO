"""Unit tests for Task model."""

from src.models.task import Task


def test_task_creation_with_all_fields():
    """Test Task creation with all fields specified."""
    task = Task(id=1, description="Test task", is_complete=True)
    assert task.id == 1
    assert task.description == "Test task"
    assert task.is_complete is True


def test_is_complete_defaults_to_false():
    """Test that is_complete defaults to False when not specified."""
    task = Task(id=1, description="Test task")
    assert task.is_complete is False


def test_task_equality():
    """Test Task equality comparison."""
    task1 = Task(id=1, description="Test task", is_complete=False)
    task2 = Task(id=1, description="Test task", is_complete=False)
    assert task1 == task2

    task3 = Task(id=2, description="Test task", is_complete=False)
    assert task1 != task3
