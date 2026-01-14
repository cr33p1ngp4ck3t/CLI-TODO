# Implementation Plan: Phase I - In-Memory Todo Console Application

**Branch**: `001-phase1-todo-app` | **Date**: 2025-12-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-phase1-todo-app/spec.md`

## Summary

Build a menu-driven Python console application for basic task management with in-memory storage. The application provides CRUD operations (add, view, update, delete) plus completion toggling for todo items, running in a continuous loop until user exit. All data is stored in memory only—no persistence, no external dependencies, no web frameworks.

## Technical Context

**Language/Version**: Python 3.13+ (per Constitution Principle IV)
**Primary Dependencies**: None (standard library only)
**Storage**: In-memory (Python list/dict data structures)
**Testing**: pytest (per Constitution Principle VIII)
**Target Platform**: Any system with Python 3.13+ and standard terminal/console
**Project Type**: Single Python program
**Performance Goals**: <1s response for all operations; supports 100+ tasks without degradation (per SC-005, SC-006)
**Constraints**: No persistence, no network, no external libraries, no database, no web framework
**Scale/Scope**: Single user, single session, in-memory only

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| I. SDD Mandate | Spec approved before planning | ✅ PASS | spec.md is complete with acceptance criteria |
| II. Agent Behavior | No feature invention | ✅ PASS | Plan implements only spec-defined features |
| III. Phase Governance | No cross-phase leakage | ✅ PASS | No DB, no web, no AI features included |
| IV. Technology Constraints | Python 3.13+, UV, no DB/web | ✅ PASS | Standard library only approach |
| VI. Feature Tiers | Basic Level only for Phase I | ✅ PASS | Only Add/Delete/Update/View/Mark Complete |
| VII. Monorepo Structure | N/A for Phase I | ✅ PASS | Single-file project, monorepo structure for Phase II+ |
| VIII. Quality Principles | Separation of concerns | ✅ PASS | Models, services, CLI layers planned |

**Gate Status**: ✅ ALL GATES PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-phase1-todo-app/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
src/
├── models/
│   └── task.py          # Task dataclass/entity
├── services/
│   └── task_service.py  # Business logic: CRUD operations
├── cli/
│   └── menu.py          # Menu display and user input handling
└── main.py              # Application entry point, main loop

tests/
├── unit/
│   ├── test_task.py     # Task model unit tests
│   └── test_task_service.py  # Service logic unit tests
└── integration/
    └── test_cli.py      # CLI integration tests (simulated I/O)
```

**Structure Decision**: Single project structure selected. Phase I is a standalone console application with no frontend/backend separation. The three-layer architecture (models → services → cli) ensures clean separation of concerns per Constitution Principle VIII.

## Architecture Design

### 1. High-Level Application Structure

The application follows a layered architecture with clear separation:

```
┌─────────────────────────────────────────┐
│              main.py                    │
│         (Entry point, main loop)        │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│              cli/menu.py                │
│    (User interface, input/output)       │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│          services/task_service.py       │
│      (Business logic, validation)       │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│            models/task.py               │
│        (Task entity definition)         │
└─────────────────────────────────────────┘
```

**Rationale**: This layered approach:
- Separates presentation (CLI) from business logic (services) from data (models)
- Makes unit testing straightforward—services can be tested without CLI
- Prepares for Phase II where the service layer can be reused with a web API

### 2. In-Memory Data Structures

**Task Storage**:
```python
# In TaskService class
_tasks: dict[int, Task]  # {task_id: Task object}
_next_id: int            # Auto-incrementing counter, starts at 1
```

**Design Decisions**:
- **Dictionary over List**: O(1) lookup by ID for update/delete/toggle operations
- **Integer keys**: Task IDs as dictionary keys for direct access
- **Counter isolation**: `_next_id` never decrements, even after deletion (per spec assumption)

**Task Entity**:
```python
@dataclass
class Task:
    id: int
    description: str
    is_complete: bool = False
```

### 3. Task Identification Strategy

**ID Generation Rules**:
- IDs are positive integers starting at 1
- Each new task receives `_next_id`, then `_next_id += 1`
- IDs are never reused after deletion (spec assumption)
- IDs are unique and immutable once assigned

**Implementation**:
```python
def add_task(self, description: str) -> Task:
    task = Task(id=self._next_id, description=description)
    self._tasks[self._next_id] = task
    self._next_id += 1
    return task
```

### 4. CLI Control Flow

**Main Loop Pattern**:
```
START
  │
  ▼
┌─────────────────┐
│  Display Menu   │◄────────────────┐
└────────┬────────┘                 │
         │                          │
         ▼                          │
┌─────────────────┐                 │
│  Get User Input │                 │
└────────┬────────┘                 │
         │                          │
         ▼                          │
┌─────────────────┐                 │
│ Validate Choice │                 │
└────────┬────────┘                 │
         │                          │
    ┌────┴────┐                     │
    │ Valid?  │                     │
    └────┬────┘                     │
    NO   │   YES                    │
    │    └───────┐                  │
    │            ▼                  │
    │   ┌────────────────┐          │
    │   │ Execute Action │          │
    │   └────────┬───────┘          │
    │            │                  │
    │   ┌────────┴────────┐         │
    │   │ Exit selected?  │         │
    │   └────────┬────────┘         │
    │       NO   │   YES            │
    │       │    └────────► END     │
    │       │                       │
    └───────┴───────────────────────┘
```

**Menu Options Mapping**:
| Input | Action | Service Method |
|-------|--------|----------------|
| 1 | Add Task | `task_service.add_task(description)` |
| 2 | View Tasks | `task_service.get_all_tasks()` |
| 3 | Update Task | `task_service.update_task(id, description)` |
| 4 | Delete Task | `task_service.delete_task(id)` |
| 5 | Mark Complete/Incomplete | `task_service.toggle_complete(id)` |
| 6 | Exit | Return from main loop |

### 5. Separation of Responsibilities

| Layer | File | Responsibility | Does NOT Handle |
|-------|------|----------------|-----------------|
| **Model** | `models/task.py` | Define Task structure, field types | Business logic, I/O |
| **Service** | `services/task_service.py` | CRUD logic, validation, ID generation, storage | User interaction, display formatting |
| **CLI** | `cli/menu.py` | Menu display, input prompts, output formatting, user feedback | Data storage, validation rules |
| **Entry** | `main.py` | Application startup, main loop orchestration | Business logic, UI details |

**Dependency Direction**: CLI → Service → Model (never reversed)

### 6. Error Handling Strategy

**Input Validation Errors**:

| Error Condition | Location | Response |
|-----------------|----------|----------|
| Empty description | `task_service.add_task()` | Raise `ValueError("Task description cannot be empty")` |
| Whitespace-only description | `task_service.add_task()` | Raise `ValueError("Task description cannot be empty")` |
| Description > 200 chars | `task_service.add_task()` | Truncate to 200 chars + "..." |
| Non-existent task ID | `task_service.get_task()` | Raise `KeyError(f"Task with ID {id} not found")` |
| Non-numeric ID input | `cli/menu.py` | Display "Please enter a valid numeric ID." and re-prompt |
| Invalid menu choice | `cli/menu.py` | Display "Invalid option. Please try again." and re-display menu |

**Empty State Handling**:

| Operation | Empty List Response |
|-----------|---------------------|
| View Tasks | "No tasks found. Add a task to get started!" |
| Update Task | "No tasks to update. Add a task first!" |
| Delete Task | "No tasks to delete. Add a task first!" |
| Mark Complete | "No tasks to update. Add a task first!" |

**Error Flow Pattern**:
```python
# In CLI layer
try:
    result = task_service.some_operation(user_input)
    display_success(result)
except ValueError as e:
    display_error(str(e))
except KeyError as e:
    display_error(str(e))
```

**Rationale**:
- Validation errors raise exceptions in the service layer
- CLI layer catches and displays user-friendly messages
- This keeps validation logic testable in isolation

## Complexity Tracking

> No violations detected. All Constitutional gates pass.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | — | — |

## Post-Design Constitution Re-Check

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. SDD Mandate | ✅ PASS | Plan derived from approved spec only |
| II. Agent Behavior | ✅ PASS | No features beyond spec; no creative additions |
| III. Phase Governance | ✅ PASS | In-memory only; no persistence, no web |
| IV. Technology Constraints | ✅ PASS | Python 3.13+, standard library only |
| VI. Feature Tiers | ✅ PASS | Basic Level features only |
| VIII. Quality Principles | ✅ PASS | 3-layer architecture, clear separation |

**Final Gate Status**: ✅ ALL GATES PASS
