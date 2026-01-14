# Research: Phase I - In-Memory Todo Console Application

**Branch**: `001-phase1-todo-app` | **Date**: 2025-12-27
**Status**: Complete

## Overview

This document consolidates research findings for the Phase I implementation. Given the constrained scope (Python standard library only, in-memory storage, console I/O), the research focuses on best practices rather than technology selection.

---

## Research Topics

### 1. Python Dataclass for Task Entity

**Decision**: Use `@dataclass` decorator from `dataclasses` module

**Rationale**:
- Built into Python standard library (3.7+)
- Automatic `__init__`, `__repr__`, `__eq__` generation
- Type hints supported natively
- No external dependencies required
- Immutable option available via `frozen=True` if needed later

**Alternatives Considered**:
| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Plain class | Full control | Boilerplate code | Rejected |
| NamedTuple | Immutable, lightweight | Less flexible for mutable fields | Rejected |
| @dataclass | Clean, type-safe, mutable | None significant | **Selected** |
| Pydantic | Validation built-in | External dependency | Rejected (Phase I constraint) |

**Implementation Pattern**:
```python
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    description: str
    is_complete: bool = False
```

---

### 2. In-Memory Storage Pattern

**Decision**: Use `dict[int, Task]` with auto-incrementing integer counter

**Rationale**:
- O(1) lookup, insert, delete by task ID
- Dictionary preserves insertion order (Python 3.7+)
- Simple integer counter ensures unique IDs
- No risk of ID collision (counter never decrements)

**Alternatives Considered**:
| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| `list[Task]` | Simple iteration | O(n) lookup by ID | Rejected |
| `dict[int, Task]` | O(1) operations | Slightly more memory | **Selected** |
| UUID keys | Globally unique | Overkill for single-session app | Rejected |

**Implementation Pattern**:
```python
class TaskService:
    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1
```

---

### 3. Console Menu Loop Pattern

**Decision**: While-loop with match-case statement (Python 3.10+)

**Rationale**:
- `match-case` provides clean, readable dispatch
- While-loop ensures continuous operation until explicit exit
- Clear separation between menu display and action execution

**Alternatives Considered**:
| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| if-elif chain | Compatible with older Python | Verbose, harder to maintain | Rejected |
| match-case | Clean, modern syntax | Requires Python 3.10+ | **Selected** |
| Dictionary dispatch | Functional approach | Less readable for CLI | Rejected |

**Implementation Pattern**:
```python
def main_loop():
    while True:
        display_menu()
        choice = get_user_choice()
        match choice:
            case "1": handle_add_task()
            case "2": handle_view_tasks()
            # ...
            case "6":
                print_goodbye()
                break
            case _: print_invalid_option()
```

---

### 4. Input Validation Strategy

**Decision**: Validate in service layer, handle errors in CLI layer

**Rationale**:
- Business rules (empty description, ID existence) belong in service layer
- User-facing messages belong in CLI layer
- Exception-based flow allows clean separation
- Service layer remains testable without I/O mocking

**Validation Rules from Spec**:
| Rule | Validation Location | Error Type |
|------|---------------------|------------|
| Non-empty description | `TaskService.add_task()` | `ValueError` |
| Task ID exists | `TaskService.get_task()` | `KeyError` |
| Numeric ID input | `cli/menu.py` | Re-prompt loop |
| Valid menu option | `cli/menu.py` | Re-prompt loop |

**Implementation Pattern**:
```python
# Service layer
def add_task(self, description: str) -> Task:
    if not description or not description.strip():
        raise ValueError("Task description cannot be empty")
    # ... create task

# CLI layer
try:
    task = service.add_task(description)
    print(f"Task {task.id} created successfully")
except ValueError as e:
    print(f"Error: {e}")
```

---

### 5. Description Truncation

**Decision**: Truncate at 200 characters, append "..." for display

**Rationale**:
- Spec requires: "Task descriptions exceeding 200 characters are truncated to 200 characters with '...' appended"
- Store full description internally (up to 200 chars)
- Display truncated version in task list

**Implementation Pattern**:
```python
MAX_DESCRIPTION_LENGTH = 200

def _normalize_description(self, description: str) -> str:
    stripped = description.strip()
    if len(stripped) > MAX_DESCRIPTION_LENGTH:
        return stripped[:MAX_DESCRIPTION_LENGTH]
    return stripped

def _format_for_display(self, description: str) -> str:
    if len(description) == MAX_DESCRIPTION_LENGTH:
        return description + "..."
    return description
```

---

### 6. Testing Strategy

**Decision**: pytest with separate unit and integration test directories

**Rationale**:
- pytest is the de facto Python testing standard
- Unit tests for service layer (no I/O)
- Integration tests for CLI (with I/O mocking via `monkeypatch` or `unittest.mock`)
- Separation allows fast unit test runs

**Test Coverage Goals**:
| Layer | Test Type | Coverage Target |
|-------|-----------|-----------------|
| `models/task.py` | Unit | 100% |
| `services/task_service.py` | Unit | 100% |
| `cli/menu.py` | Integration | Key paths |
| `main.py` | Integration | Smoke test |

**Implementation Pattern**:
```python
# tests/unit/test_task_service.py
def test_add_task_creates_task_with_incremented_id():
    service = TaskService()
    task1 = service.add_task("First task")
    task2 = service.add_task("Second task")
    assert task1.id == 1
    assert task2.id == 2

def test_add_task_raises_on_empty_description():
    service = TaskService()
    with pytest.raises(ValueError, match="cannot be empty"):
        service.add_task("")
```

---

## Resolved Clarifications

All Technical Context items from the plan template have been resolved:

| Item | Resolution |
|------|------------|
| Language/Version | Python 3.13+ (Constitution mandate) |
| Dependencies | None (standard library only) |
| Storage | In-memory dict (this document) |
| Testing | pytest (this document) |
| Target Platform | Any terminal with Python 3.13+ |

---

## Summary

Phase I implementation requires no external research beyond Python standard library best practices. All architectural decisions align with:
- Constitution Principle IV (Technology Constraints)
- Constitution Principle VIII (Quality Principles)
- Spec FR-013 (In-memory storage only)

**Next Step**: Proceed to Phase 1 (data-model.md, quickstart.md)
