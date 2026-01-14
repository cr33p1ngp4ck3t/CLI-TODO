"""Task service for managing todo items."""

from src.models.task import Task


class TaskService:
    """Manages in-memory task storage and CRUD operations.

    Attributes:
        _tasks: Dictionary mapping task IDs to Task objects
        _next_id: Counter for generating unique task IDs
    """

    def __init__(self) -> None:
        """Initialize empty task storage with ID counter starting at 1."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def is_empty(self) -> bool:
        """Check if the task list is empty.

        Returns:
            True if no tasks exist, False otherwise
        """
        return len(self._tasks) == 0

    def add_task(self, description: str) -> Task:
        """Create a new task with the given description.

        Args:
            description: Task description (1-200 chars, non-empty)

        Returns:
            The newly created Task with auto-generated ID

        Raises:
            ValueError: If description is empty or whitespace-only
        """
        # Validate description
        if not description or not description.strip():
            raise ValueError("Task description cannot be empty")

        # Strip and truncate description
        description = description.strip()
        if len(description) > 200:
            description = description[:200]

        # Create and store task
        task = Task(id=self._next_id, description=description, is_complete=False)
        self._tasks[self._next_id] = task
        self._next_id += 1

        return task

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks in insertion order.

        Returns:
            List of all tasks (empty list if no tasks exist)
        """
        return list(self._tasks.values())

    def get_task(self, task_id: int) -> Task:
        """Retrieve a task by its ID.

        Args:
            task_id: The unique task identifier

        Returns:
            The Task with the given ID

        Raises:
            KeyError: If no task exists with the given ID
        """
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} not found")
        return self._tasks[task_id]

    def toggle_complete(self, task_id: int) -> Task:
        """Toggle the completion status of a task.

        Args:
            task_id: The unique task identifier

        Returns:
            The updated Task with toggled is_complete status

        Raises:
            KeyError: If no task exists with the given ID
        """
        task = self.get_task(task_id)
        task.is_complete = not task.is_complete
        return task

    def update_task(self, task_id: int, description: str) -> Task:
        """Update the description of an existing task.

        Args:
            task_id: The unique task identifier
            description: New description (1-200 chars, non-empty)

        Returns:
            The updated Task

        Raises:
            KeyError: If no task exists with the given ID
            ValueError: If description is empty or whitespace-only
        """
        # Validate description
        if not description or not description.strip():
            raise ValueError("Task description cannot be empty")

        # Strip and truncate description
        description = description.strip()
        if len(description) > 200:
            description = description[:200]

        # Update task
        task = self.get_task(task_id)
        task.description = description
        return task

    def delete_task(self, task_id: int) -> None:
        """Delete a task by its ID.

        Args:
            task_id: The unique task identifier

        Raises:
            KeyError: If no task exists with the given ID
        """
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} not found")
        del self._tasks[task_id]
