# Data Model: Phase I - In-Memory Todo Console Application

**Branch**: `001-phase1-todo-app` | **Date**: 2025-12-27
**Status**: Complete

## Overview

This document defines the data model for the Phase I Todo application. The model is intentionally minimal, covering only the Task entity and its in-memory storage structure.

---

## Entities

### Task

The core entity representing a single todo item.

**Source**: spec.md, Key Entities section

```python
from dataclasses import dataclass

@dataclass
class Task:
    """Represents a single todo item in the application."""

    id: int
    """Unique identifier, auto-generated, starts at 1, increments for each new task."""

    description: str
    """Text describing the task, 1-200 characters, required, non-empty."""

    is_complete: bool = False
    """Completion status, defaults to False when created."""
```

#### Field Specifications

| Field | Type | Constraints | Default | Source |
|-------|------|-------------|---------|--------|
| `id` | `int` | Positive integer, unique, immutable | Auto-generated | FR-003 |
| `description` | `str` | 1-200 characters, non-empty, non-whitespace-only | Required | FR-002, FR-008 |
| `is_complete` | `bool` | True/False | `False` | FR-005 |

#### Validation Rules

| Rule | Enforcement | Error Message |
|------|-------------|---------------|
| Description not empty | `TaskService.add_task()` | "Task description cannot be empty" |
| Description not whitespace-only | `TaskService.add_task()` | "Task description cannot be empty" |
| Description max 200 chars | `TaskService.add_task()` | Truncated silently (per Edge Cases) |
| ID must exist for operations | `TaskService.*` methods | "Task with ID {id} not found" |

#### State Transitions

```
┌─────────────────┐
│   INCOMPLETE    │◄─────────────┐
│  is_complete=   │              │
│     False       │              │
└────────┬────────┘              │
         │                       │
         │ toggle_complete()     │ toggle_complete()
         │                       │
         ▼                       │
┌─────────────────┐              │
│    COMPLETE     │──────────────┘
│  is_complete=   │
│     True        │
└─────────────────┘
```

---

## Storage Structure

### TaskService Internal State

The `TaskService` class manages all task storage and operations.

```python
class TaskService:
    """Manages in-memory task storage and CRUD operations."""

    _tasks: dict[int, Task]
    """Dictionary mapping task IDs to Task objects. Provides O(1) lookup."""

    _next_id: int
    """Counter for generating unique task IDs. Starts at 1, only increments."""
```

#### Storage Invariants

| Invariant | Description |
|-----------|-------------|
| Unique IDs | No two tasks share the same ID |
| ID Monotonicity | `_next_id` only increases, never decreases |
| ID Gap Tolerance | Deleted task IDs are not reused |
| Order Preservation | Tasks maintain insertion order (Python 3.7+ dict behavior) |

#### Memory Characteristics

| Metric | Value | Rationale |
|--------|-------|-----------|
| Max Tasks | 100+ (per SC-006) | Spec requires no degradation at 100 tasks |
| Task Size | ~300 bytes estimated | id (28B) + description (up to 200 chars) + bool (28B) + overhead |
| Total Memory | <50KB for 100 tasks | Well within acceptable limits |

---

## Service Interface

### TaskService Methods

```python
class TaskService:
    def __init__(self) -> None:
        """Initialize empty task storage with ID counter starting at 1."""

    def add_task(self, description: str) -> Task:
        """
        Create a new task with the given description.

        Args:
            description: Task description (1-200 chars, non-empty)

        Returns:
            The newly created Task with auto-generated ID

        Raises:
            ValueError: If description is empty or whitespace-only
        """

    def get_task(self, task_id: int) -> Task:
        """
        Retrieve a task by its ID.

        Args:
            task_id: The unique task identifier

        Returns:
            The Task with the given ID

        Raises:
            KeyError: If no task exists with the given ID
        """

    def get_all_tasks(self) -> list[Task]:
        """
        Retrieve all tasks in insertion order.

        Returns:
            List of all tasks (empty list if no tasks exist)
        """

    def update_task(self, task_id: int, description: str) -> Task:
        """
        Update the description of an existing task.

        Args:
            task_id: The unique task identifier
            description: New description (1-200 chars, non-empty)

        Returns:
            The updated Task

        Raises:
            KeyError: If no task exists with the given ID
            ValueError: If description is empty or whitespace-only
        """

    def delete_task(self, task_id: int) -> None:
        """
        Delete a task by its ID.

        Args:
            task_id: The unique task identifier

        Raises:
            KeyError: If no task exists with the given ID
        """

    def toggle_complete(self, task_id: int) -> Task:
        """
        Toggle the completion status of a task.

        Args:
            task_id: The unique task identifier

        Returns:
            The updated Task with toggled is_complete status

        Raises:
            KeyError: If no task exists with the given ID
        """

    def is_empty(self) -> bool:
        """
        Check if the task list is empty.

        Returns:
            True if no tasks exist, False otherwise
        """
```

---

## Display Format

### Task List Display

When displaying tasks (FR-004), each task shows:

```
[{status}] ID: {id} - {description}
```

Where:
- `{status}` = `✓` if complete, ` ` (space) if incomplete
- `{id}` = Task ID (integer)
- `{description}` = Task description (truncated to 200 chars + "..." if needed)

**Example Output**:
```
[ ] ID: 1 - Buy groceries
[✓] ID: 2 - Call dentist
[ ] ID: 3 - Finish report for quarterly review meeting with stakeholders...
```

---

## Relationships

Phase I has no entity relationships (single entity: Task).

Future phases will introduce:
- User → Task (Phase II: user authentication)
- Task → Category (Phase II+: tags/priorities)

---

## Summary

| Aspect | Decision |
|--------|----------|
| Entity | Single `Task` dataclass |
| Storage | `dict[int, Task]` in `TaskService` |
| ID Strategy | Auto-incrementing integer, never reused |
| Validation | Service layer, raises exceptions |
| State | Binary: complete/incomplete (toggle) |
