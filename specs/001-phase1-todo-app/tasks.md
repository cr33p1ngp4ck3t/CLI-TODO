# Tasks: Phase I - In-Memory Todo Console Application

**Input**: Design documents from `/specs/001-phase1-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, quickstart.md

**Branch**: `001-phase1-todo-app`
**Date**: 2025-12-27

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Exact file paths included in descriptions

## Path Conventions

Per plan.md Section "Source Code":
- **Source**: `src/` at repository root
- **Tests**: `tests/` at repository root

---

## Phase 1: Setup (Project Infrastructure)

**Purpose**: Initialize project structure and Python environment

**Spec Reference**: plan.md Section "Project Structure"

- [ ] T001 Create project directory structure per plan.md
  - **Preconditions**: Repository cloned, branch `001-phase1-todo-app` checked out
  - **Expected Output**: All directories exist: `src/`, `src/models/`, `src/services/`, `src/cli/`, `tests/`, `tests/unit/`, `tests/integration/`
  - **Artifacts**:
    - `src/__init__.py`
    - `src/models/__init__.py`
    - `src/services/__init__.py`
    - `src/cli/__init__.py`
    - `tests/__init__.py`
    - `tests/unit/__init__.py`
    - `tests/integration/__init__.py`

- [ ] T002 Initialize UV project with pytest dependency
  - **Preconditions**: T001 complete, UV installed
  - **Expected Output**: `pyproject.toml` exists with Python 3.13+ requirement and pytest dev dependency
  - **Artifacts**: `pyproject.toml`
  - **Spec Reference**: plan.md Technical Context (Python 3.13+, pytest)

- [ ] T002A Add rich library for enhanced CLI UI
  - **Preconditions**: T002 complete
  - **Expected Output**: `rich` package added as production dependency in `pyproject.toml`
  - **Artifacts**: `pyproject.toml` (modify)
  - **Rationale**: Rich provides enhanced terminal formatting, colors, tables, and progress indicators for better user experience

- [ ] T002B Add pyfiglet for ASCII art text rendering
  - **Preconditions**: T002 complete
  - **Expected Output**: `pyfiglet` package added as production dependency in `pyproject.toml`
  - **Artifacts**: `pyproject.toml` (modify)
  - **Rationale**: Pyfiglet enables ASCII art text generation for application header and branding

**Checkpoint**: Project structure ready for implementation

---

## Phase 2: Foundational (Core Model & Service)

**Purpose**: Create Task entity and TaskService that all user stories depend on

**⚠️ CRITICAL**: All user story implementations depend on this phase

### Task Model

- [ ] T003 [FOUND] Create Task dataclass in `src/models/task.py`
  - **Preconditions**: T001 complete
  - **Expected Output**: Task dataclass with `id: int`, `description: str`, `is_complete: bool = False`
  - **Artifacts**: `src/models/task.py`
  - **Spec Reference**: spec.md Key Entities, data-model.md Task Entity
  - **Acceptance Criteria**:
    - [ ] Task has `id` field (int, required)
    - [ ] Task has `description` field (str, required)
    - [ ] Task has `is_complete` field (bool, default False)
    - [ ] Uses `@dataclass` decorator

- [ ] T004 [FOUND] Export Task from models package
  - **Preconditions**: T003 complete
  - **Expected Output**: `from src.models import Task` works
  - **Artifacts**: `src/models/__init__.py` (modify)

### Task Service Foundation

- [ ] T005 [FOUND] Create TaskService class skeleton in `src/services/task_service.py`
  - **Preconditions**: T003, T004 complete
  - **Expected Output**: TaskService class with `_tasks: dict[int, Task]` and `_next_id: int = 1`
  - **Artifacts**: `src/services/task_service.py`
  - **Spec Reference**: plan.md Section 2 "In-Memory Data Structures", data-model.md Storage Structure
  - **Acceptance Criteria**:
    - [ ] `__init__` initializes empty `_tasks` dict
    - [ ] `__init__` sets `_next_id = 1`
    - [ ] `is_empty() -> bool` method returns True when no tasks

- [ ] T006 [FOUND] Export TaskService from services package
  - **Preconditions**: T005 complete
  - **Expected Output**: `from src.services import TaskService` works
  - **Artifacts**: `src/services/__init__.py` (modify)

### Unit Tests for Foundation

- [ ] T007 [P] [FOUND] Create unit tests for Task model in `tests/unit/test_task.py`
  - **Preconditions**: T003 complete
  - **Expected Output**: Tests pass for Task creation, default values
  - **Artifacts**: `tests/unit/test_task.py`
  - **Test Cases**:
    - [ ] Test Task creation with all fields
    - [ ] Test `is_complete` defaults to False
    - [ ] Test Task equality

- [ ] T008 [FOUND] Create unit tests for TaskService initialization in `tests/unit/test_task_service.py`
  - **Preconditions**: T005 complete
  - **Expected Output**: Tests pass for service initialization
  - **Artifacts**: `tests/unit/test_task_service.py`
  - **Test Cases**:
    - [ ] Test `is_empty()` returns True on new service
    - [ ] Test `_next_id` starts at 1

**Checkpoint**: Foundation ready - User story implementation can begin

---

## Phase 3: User Story 1 - Add a New Task (Priority: P1)

**Goal**: Users can add tasks to their todo list
**Spec Reference**: spec.md User Story 1, FR-002, FR-003, FR-008

**Independent Test**: Launch app → Select "Add Task" → Enter description → Verify task appears in list

### Service Implementation

- [ ] T009 [US1] Implement `add_task(description: str) -> Task` in TaskService
  - **Preconditions**: T005 complete
  - **Expected Output**: Method creates task with auto-incremented ID, stores in `_tasks`
  - **Artifacts**: `src/services/task_service.py` (modify)
  - **Spec Reference**: plan.md Section 3 "Task Identification Strategy", FR-003
  - **Acceptance Criteria**:
    - [ ] Assigns `_next_id` to new task
    - [ ] Increments `_next_id` after assignment
    - [ ] Stores task in `_tasks` dict
    - [ ] Returns created Task object

- [ ] T010 [US1] Add description validation to `add_task()`
  - **Preconditions**: T009 complete
  - **Expected Output**: Raises `ValueError` for empty/whitespace descriptions
  - **Artifacts**: `src/services/task_service.py` (modify)
  - **Spec Reference**: plan.md Section 6 "Error Handling Strategy", FR-008
  - **Acceptance Criteria**:
    - [ ] Raises `ValueError("Task description cannot be empty")` for empty string
    - [ ] Raises `ValueError("Task description cannot be empty")` for whitespace-only
    - [ ] Strips leading/trailing whitespace from valid descriptions

- [ ] T011 [US1] Add description truncation to `add_task()`
  - **Preconditions**: T010 complete
  - **Expected Output**: Descriptions > 200 chars truncated to 200 chars
  - **Artifacts**: `src/services/task_service.py` (modify)
  - **Spec Reference**: spec.md Edge Cases "Very long task description"
  - **Acceptance Criteria**:
    - [ ] Descriptions ≤ 200 chars stored as-is
    - [ ] Descriptions > 200 chars truncated to exactly 200 chars

### Unit Tests for Add Task

- [ ] T012 [US1] Add unit tests for `add_task()` in `tests/unit/test_task_service.py`
  - **Preconditions**: T011 complete
  - **Expected Output**: All add_task tests pass
  - **Artifacts**: `tests/unit/test_task_service.py` (modify)
  - **Test Cases**:
    - [ ] Test task created with correct description
    - [ ] Test task assigned ID 1 on first add
    - [ ] Test second task assigned ID 2
    - [ ] Test `is_empty()` returns False after add
    - [ ] Test `ValueError` raised for empty description
    - [ ] Test `ValueError` raised for whitespace-only description
    - [ ] Test description truncated at 200 chars

**Checkpoint**: add_task service method complete and tested

---

## Phase 4: User Story 2 - View Task List (Priority: P1)

**Goal**: Users can see all their tasks with ID, description, and status
**Spec Reference**: spec.md User Story 2, FR-004

**Independent Test**: Add tasks → Select "View Tasks" → Verify all tasks displayed

### Service Implementation

- [ ] T013 [US2] Implement `get_all_tasks() -> list[Task]` in TaskService
  - **Preconditions**: T005 complete
  - **Expected Output**: Returns list of all tasks in insertion order
  - **Artifacts**: `src/services/task_service.py` (modify)
  - **Spec Reference**: data-model.md TaskService Methods
  - **Acceptance Criteria**:
    - [ ] Returns empty list when no tasks
    - [ ] Returns tasks in insertion order (dict preserves order in Python 3.7+)
    - [ ] Returns list copy, not internal dict values

### Unit Tests for View Tasks

- [ ] T014 [US2] Add unit tests for `get_all_tasks()` in `tests/unit/test_task_service.py`
  - **Preconditions**: T013 complete
  - **Expected Output**: All get_all_tasks tests pass
  - **Artifacts**: `tests/unit/test_task_service.py` (modify)
  - **Test Cases**:
    - [ ] Test returns empty list when no tasks
    - [ ] Test returns all added tasks
    - [ ] Test tasks returned in insertion order

**Checkpoint**: get_all_tasks service method complete and tested

---

## Phase 5: User Story 3 - Mark Task Complete/Incomplete (Priority: P2)

**Goal**: Users can toggle task completion status
**Spec Reference**: spec.md User Story 3, FR-005

**Independent Test**: Add task → Mark complete → View (shows complete) → Mark incomplete → View (shows incomplete)

### Service Implementation

- [ ] T015 [US3] Implement `get_task(task_id: int) -> Task` in TaskService
  - **Preconditions**: T005 complete
  - **Expected Output**: Returns task by ID or raises KeyError
  - **Artifacts**: `src/services/task_service.py` (modify)
  - **Spec Reference**: data-model.md TaskService Methods, FR-009
  - **Acceptance Criteria**:
    - [ ] Returns Task when ID exists
    - [ ] Raises `KeyError(f"Task with ID {task_id} not found")` when ID not found

- [ ] T016 [US3] Implement `toggle_complete(task_id: int) -> Task` in TaskService
  - **Preconditions**: T015 complete
  - **Expected Output**: Toggles `is_complete` and returns updated task
  - **Artifacts**: `src/services/task_service.py` (modify)
  - **Spec Reference**: data-model.md State Transitions, FR-005
  - **Acceptance Criteria**:
    - [ ] If task `is_complete=False`, sets to `True`
    - [ ] If task `is_complete=True`, sets to `False`
    - [ ] Raises `KeyError` if task not found
    - [ ] Returns updated Task

### Unit Tests for Toggle Complete

- [ ] T017 [US3] Add unit tests for `get_task()` and `toggle_complete()` in `tests/unit/test_task_service.py`
  - **Preconditions**: T016 complete
  - **Expected Output**: All toggle tests pass
  - **Artifacts**: `tests/unit/test_task_service.py` (modify)
  - **Test Cases**:
    - [ ] Test `get_task` returns correct task
    - [ ] Test `get_task` raises KeyError for non-existent ID
    - [ ] Test toggle changes False to True
    - [ ] Test toggle changes True to False
    - [ ] Test toggle raises KeyError for non-existent ID

**Checkpoint**: toggle_complete service method complete and tested

---

## Phase 6: User Story 4 - Update Task Description (Priority: P3)

**Goal**: Users can modify existing task descriptions
**Spec Reference**: spec.md User Story 4, FR-006

**Independent Test**: Add task → Update description → View (shows new description)

### Service Implementation

- [ ] T018 [US4] Implement `update_task(task_id: int, description: str) -> Task` in TaskService
  - **Preconditions**: T015, T010 complete
  - **Expected Output**: Updates description, returns updated task
  - **Artifacts**: `src/services/task_service.py` (modify)
  - **Spec Reference**: data-model.md TaskService Methods, FR-006
  - **Acceptance Criteria**:
    - [ ] Raises `KeyError` if task not found
    - [ ] Raises `ValueError` if description empty/whitespace
    - [ ] Truncates description > 200 chars
    - [ ] Updates task description in storage
    - [ ] Returns updated Task

### Unit Tests for Update Task

- [ ] T019 [US4] Add unit tests for `update_task()` in `tests/unit/test_task_service.py`
  - **Preconditions**: T018 complete
  - **Expected Output**: All update tests pass
  - **Artifacts**: `tests/unit/test_task_service.py` (modify)
  - **Test Cases**:
    - [ ] Test description updated successfully
    - [ ] Test raises KeyError for non-existent ID
    - [ ] Test raises ValueError for empty description
    - [ ] Test description truncated at 200 chars

**Checkpoint**: update_task service method complete and tested

---

## Phase 7: User Story 5 - Delete Task (Priority: P3)

**Goal**: Users can remove tasks from their list
**Spec Reference**: spec.md User Story 5, FR-007

**Independent Test**: Add task → Delete task → View (task not present)

### Service Implementation

- [ ] T020 [US5] Implement `delete_task(task_id: int) -> None` in TaskService
  - **Preconditions**: T015 complete
  - **Expected Output**: Removes task from storage
  - **Artifacts**: `src/services/task_service.py` (modify)
  - **Spec Reference**: data-model.md TaskService Methods, FR-007
  - **Acceptance Criteria**:
    - [ ] Raises `KeyError` if task not found
    - [ ] Removes task from `_tasks` dict
    - [ ] Does NOT decrement `_next_id` (IDs never reused)

### Unit Tests for Delete Task

- [ ] T021 [US5] Add unit tests for `delete_task()` in `tests/unit/test_task_service.py`
  - **Preconditions**: T020 complete
  - **Expected Output**: All delete tests pass
  - **Artifacts**: `tests/unit/test_task_service.py` (modify)
  - **Test Cases**:
    - [ ] Test task removed from storage
    - [ ] Test raises KeyError for non-existent ID
    - [ ] Test ID not reused after deletion (add new task gets next ID)

**Checkpoint**: All service methods complete and tested

---

## Phase 8: CLI Menu System

**Purpose**: Build the menu display and input handling layer with enhanced UI using Rich and ASCII art
**Spec Reference**: spec.md CLI Interaction Flow, plan.md Section 4 "CLI Control Flow"

### Menu Display

- [ ] T022 [CLI] Create ASCII art header using pyfiglet in `src/cli/menu.py`
  - **Preconditions**: T001, T002B complete
  - **Expected Output**: Function generates ASCII art title "TODO APP" using pyfiglet
  - **Artifacts**: `src/cli/menu.py`
  - **Acceptance Criteria**:
    - [ ] Uses pyfiglet to render "TODO APP" in ASCII art
    - [ ] Falls back to plain text if pyfiglet unavailable
    - [ ] Returns formatted string

- [ ] T022A [CLI] Create enhanced menu display using Rich in `src/cli/menu.py`
  - **Preconditions**: T022, T002A complete
  - **Expected Output**: Function displays styled menu using Rich Panel and Table components
  - **Artifacts**: `src/cli/menu.py` (modify)
  - **Spec Reference**: spec.md CLI Interaction Flow
  - **Acceptance Criteria**:
    - [ ] Displays ASCII art header from T022
    - [ ] Uses Rich Panel to frame the menu
    - [ ] Uses Rich Table to display menu options (1-6) with colors
    - [ ] Options: 1. Add Task, 2. View Tasks, 3. Update Task, 4. Delete Task, 5. Mark Complete/Incomplete, 6. Exit
    - [ ] Applies color scheme: cyan for headers, green for options, yellow for prompts

- [ ] T023 [CLI] Create user choice input function using Rich Prompt in `src/cli/menu.py`
  - **Preconditions**: T022A complete
  - **Expected Output**: Function prompts with styled text using Rich and returns input
  - **Artifacts**: `src/cli/menu.py` (modify)
  - **Spec Reference**: spec.md CLI Interaction Flow
  - **Acceptance Criteria**:
    - [ ] Uses Rich Prompt.ask() for styled input
    - [ ] Prompts with "Enter your choice" with color styling
    - [ ] Validates input is in range 1-6
    - [ ] Returns user input as string

### Input Helpers

- [ ] T024 [CLI] Create task ID input helper using Rich Prompt in `src/cli/menu.py`
  - **Preconditions**: T023 complete
  - **Expected Output**: Function prompts for ID with Rich styling, validates numeric input, re-prompts on invalid
  - **Artifacts**: `src/cli/menu.py` (modify)
  - **Spec Reference**: plan.md Section 6 "Error Handling Strategy", spec.md Edge Cases "Non-numeric ID input"
  - **Acceptance Criteria**:
    - [ ] Uses Rich IntPrompt for numeric validation
    - [ ] Prompts "Enter task ID" with color styling
    - [ ] Returns integer on valid numeric input
    - [ ] Displays styled error message and re-prompts on invalid input

- [ ] T025 [CLI] Create description input helper using Rich Prompt in `src/cli/menu.py`
  - **Preconditions**: T024 complete
  - **Expected Output**: Function prompts for description with Rich styling, returns string
  - **Artifacts**: `src/cli/menu.py` (modify)
  - **Acceptance Criteria**:
    - [ ] Uses Rich Prompt.ask() for styled input
    - [ ] Prompts "Enter task description" with color styling (for add)
    - [ ] Prompts "Enter new description" with color styling (for update, passed as parameter)
    - [ ] Returns user input as string

### Export CLI Functions

- [ ] T026 [CLI] Export CLI functions from cli package
  - **Preconditions**: T025 complete
  - **Expected Output**: `from src.cli import display_menu, get_user_choice, ...` works
  - **Artifacts**: `src/cli/__init__.py` (modify)

**Checkpoint**: CLI menu components ready

---

## Phase 9: CLI Action Handlers

**Purpose**: Connect menu choices to service operations with user feedback
**Spec Reference**: plan.md Section 5 "Separation of Responsibilities"

### Handler Functions

- [ ] T027 [US1] [CLI] Implement add task handler with Rich styling in `src/cli/menu.py`
  - **Preconditions**: T009, T025, T002A complete
  - **Expected Output**: Prompts for description, calls service, displays styled result
  - **Artifacts**: `src/cli/menu.py` (modify)
  - **Spec Reference**: spec.md User Story 1 Acceptance Scenarios
  - **Acceptance Criteria**:
    - [ ] Prompts for description using Rich styled prompt
    - [ ] Calls `task_service.add_task(description)`
    - [ ] On success: displays "✓ Task {id} created successfully" in green using Rich console
    - [ ] On ValueError: displays error message in red using Rich console

- [ ] T028 [US2] [CLI] Implement view tasks handler using Rich Table in `src/cli/menu.py`
  - **Preconditions**: T013, T002A complete
  - **Expected Output**: Displays all tasks in styled Rich Table or empty message
  - **Artifacts**: `src/cli/menu.py` (modify)
  - **Spec Reference**: spec.md User Story 2 Acceptance Scenarios, data-model.md Display Format
  - **Acceptance Criteria**:
    - [ ] Calls `task_service.get_all_tasks()`
    - [ ] If empty: displays styled message "No tasks found. Add a task to get started!" using Rich
    - [ ] If tasks exist: creates Rich Table with columns: Status, ID, Description
    - [ ] Status column shows "✓" (green) for complete, "○" (yellow) for incomplete
    - [ ] Table uses box styling and colors (green for complete rows, default for incomplete)
    - [ ] Table header uses bold cyan styling

- [ ] T029 [US4] [CLI] Implement update task handler with Rich styling in `src/cli/menu.py`
  - **Preconditions**: T018, T024, T025, T002A complete
  - **Expected Output**: Prompts for ID and description, calls service, displays styled result
  - **Artifacts**: `src/cli/menu.py` (modify)
  - **Spec Reference**: spec.md User Story 4 Acceptance Scenarios
  - **Acceptance Criteria**:
    - [ ] Checks if task list empty first: displays styled warning "⚠ No tasks to update. Add a task first!" in yellow
    - [ ] Prompts for task ID using Rich IntPrompt
    - [ ] Prompts for new description using Rich Prompt
    - [ ] On success: displays "✓ Task {id} updated successfully" in green
    - [ ] On KeyError: displays "✗ Task with ID {id} not found" in red
    - [ ] On ValueError: displays error message in red

- [ ] T030 [US5] [CLI] Implement delete task handler with Rich styling in `src/cli/menu.py`
  - **Preconditions**: T020, T024, T002A complete
  - **Expected Output**: Prompts for ID, calls service, displays styled result
  - **Artifacts**: `src/cli/menu.py` (modify)
  - **Spec Reference**: spec.md User Story 5 Acceptance Scenarios
  - **Acceptance Criteria**:
    - [ ] Checks if task list empty first: displays styled warning "⚠ No tasks to delete. Add a task first!" in yellow
    - [ ] Prompts for task ID using Rich IntPrompt
    - [ ] On success: displays "✓ Task {id} deleted successfully" in green
    - [ ] On KeyError: displays "✗ Task with ID {id} not found" in red

- [ ] T031 [US3] [CLI] Implement toggle complete handler with Rich styling in `src/cli/menu.py`
  - **Preconditions**: T016, T024, T002A complete
  - **Expected Output**: Prompts for ID, calls service, displays styled result
  - **Artifacts**: `src/cli/menu.py` (modify)
  - **Spec Reference**: spec.md User Story 3 Acceptance Scenarios
  - **Acceptance Criteria**:
    - [ ] Checks if task list empty first: displays styled warning "⚠ No tasks to update. Add a task first!" in yellow
    - [ ] Prompts for task ID using Rich IntPrompt
    - [ ] On success: displays "✓ Task {id} marked as {complete/incomplete}" in green
    - [ ] On KeyError: displays "✗ Task with ID {id} not found" in red

**Checkpoint**: All CLI handlers implemented

---

## Phase 10: Application Entry Point & Main Loop

**Purpose**: Wire together CLI and service in main application loop
**Spec Reference**: plan.md Section 4 "CLI Control Flow", FR-011, FR-012

### Main Application

- [ ] T032 [US6] Create main application loop with Rich Console in `src/main.py`
  - **Preconditions**: T026, T027-T031, T002A complete
  - **Expected Output**: Application runs continuous menu loop until exit with Rich styling
  - **Artifacts**: `src/main.py`
  - **Spec Reference**: plan.md Section 4 "Main Loop Pattern", FR-012
  - **Acceptance Criteria**:
    - [ ] Creates Rich Console instance for the application
    - [ ] Creates TaskService instance
    - [ ] Clears screen between operations using Rich console
    - [ ] Displays menu in loop
    - [ ] Dispatches to correct handler based on choice (1-6)
    - [ ] Displays styled error "⚠ Invalid option. Please try again." in yellow for invalid choices
    - [ ] Continues loop after each action

- [ ] T033 [US6] Implement exit handler with Rich styling in `src/main.py`
  - **Preconditions**: T032, T002A complete
  - **Expected Output**: Exit choice displays styled goodbye message and terminates
  - **Artifacts**: `src/main.py` (modify)
  - **Spec Reference**: spec.md User Story 6 Acceptance Scenarios, FR-011
  - **Acceptance Criteria**:
    - [ ] On choice "6": displays styled panel with "👋 Goodbye! Your tasks have not been saved." in cyan using Rich
    - [ ] Uses Rich Panel for the goodbye message
    - [ ] Breaks from main loop (application terminates)

- [ ] T034 Add `if __name__ == "__main__"` guard to `src/main.py`
  - **Preconditions**: T033 complete
  - **Expected Output**: Application runs when executed directly
  - **Artifacts**: `src/main.py` (modify)
  - **Acceptance Criteria**:
    - [ ] `python -m src.main` starts the application
    - [ ] Import of main.py does not auto-run application

**Checkpoint**: Application fully runnable

---

## Phase 11: Integration Tests

**Purpose**: Verify end-to-end user workflows
**Spec Reference**: spec.md Success Criteria SC-003, SC-004

- [ ] T035 [P] Create CLI integration test infrastructure in `tests/integration/test_cli.py`
  - **Preconditions**: T034 complete
  - **Expected Output**: Test fixtures for simulating user input/output
  - **Artifacts**: `tests/integration/test_cli.py`
  - **Acceptance Criteria**:
    - [ ] Uses `monkeypatch` or `unittest.mock` to simulate input
    - [ ] Captures stdout for verification

- [ ] T036 [P] Add integration test: Add task workflow
  - **Preconditions**: T035 complete
  - **Expected Output**: Test passes for complete add workflow
  - **Artifacts**: `tests/integration/test_cli.py` (modify)
  - **Test Case**: Select Add → Enter description → Verify success message

- [ ] T037 [P] Add integration test: View tasks workflow
  - **Preconditions**: T035 complete
  - **Expected Output**: Test passes for view workflow
  - **Artifacts**: `tests/integration/test_cli.py` (modify)
  - **Test Cases**:
    - View empty list → "No tasks found" message
    - Add task then view → task displayed

- [ ] T038 [P] Add integration test: Complete workflow (SC-003)
  - **Preconditions**: T035 complete
  - **Expected Output**: Test passes for full workflow
  - **Artifacts**: `tests/integration/test_cli.py` (modify)
  - **Test Case**: Add → View → Mark Complete → Delete → Exit (per SC-003)

- [ ] T039 [P] Add integration test: Error handling (SC-004)
  - **Preconditions**: T035 complete
  - **Expected Output**: Test passes for error cases
  - **Artifacts**: `tests/integration/test_cli.py` (modify)
  - **Test Cases**:
    - Empty description error
    - Non-existent ID error
    - Invalid menu option error

**Checkpoint**: Integration tests complete

---

## Phase 12: Final Validation

**Purpose**: Ensure all acceptance criteria met
**Spec Reference**: spec.md Success Criteria

- [ ] T040 Run all unit tests and verify 100% pass
  - **Preconditions**: All T007-T021 complete
  - **Expected Output**: `pytest tests/unit/ -v` shows all tests pass
  - **Artifacts**: None (validation only)

- [ ] T041 Run all integration tests and verify 100% pass
  - **Preconditions**: T039 complete
  - **Expected Output**: `pytest tests/integration/ -v` shows all tests pass
  - **Artifacts**: None (validation only)

- [ ] T042 Manual validation against quickstart.md
  - **Preconditions**: T041 complete
  - **Expected Output**: All quickstart verification steps pass
  - **Artifacts**: None (validation only)
  - **Steps from quickstart.md**:
    - [ ] Add a task ("Buy groceries")
    - [ ] View tasks (task appears)
    - [ ] Mark complete (shows ✓)
    - [ ] Exit (goodbye message, terminates)

- [ ] T043 Verify Success Criteria SC-005 (response time < 1s)
  - **Preconditions**: T042 complete
  - **Expected Output**: All operations respond within 1 second
  - **Artifacts**: None (validation only)
  - **Spec Reference**: spec.md SC-005

**Checkpoint**: Phase I implementation complete and validated

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    │
    ▼
Phase 2 (Foundational) ─────────────────────────────┐
    │                                               │
    ├───► Phase 3 (US1: Add Task) ──────────────────┤
    │                                               │
    ├───► Phase 4 (US2: View Tasks) ────────────────┤
    │                                               │
    ├───► Phase 5 (US3: Toggle Complete) ───────────┤
    │                                               │
    ├───► Phase 6 (US4: Update Task) ───────────────┤
    │                                               │
    └───► Phase 7 (US5: Delete Task) ───────────────┤
                                                    │
                                                    ▼
                                        Phase 8 (CLI Menu)
                                                    │
                                                    ▼
                                        Phase 9 (CLI Handlers)
                                                    │
                                                    ▼
                                        Phase 10 (Main Loop)
                                                    │
                                                    ▼
                                        Phase 11 (Integration Tests)
                                                    │
                                                    ▼
                                        Phase 12 (Validation)
```

### Task Dependencies (Critical Path)

1. **T001** → T002 → T003 → T004 → T005 → T006 (Setup + Foundation)
2. T006 → **T009 → T010 → T011** (Add Task service)
3. T006 → **T013** (View Tasks service)
4. T006 → **T015 → T016** (Toggle service)
5. T015 → **T018** (Update service)
6. T015 → **T020** (Delete service)
7. T022 → T023 → T024 → T025 → **T026** (CLI components)
8. T026 + All service methods → **T027-T031** (CLI handlers)
9. T031 → **T032 → T033 → T034** (Main loop)
10. T034 → **T035-T039** (Integration tests)
11. T039 → **T040-T043** (Validation)

### Parallel Opportunities

**Within Phase 2**:
- T007 (Task model tests) can run parallel to T008 (Service init tests)

**Within Phases 3-7** (after T006 complete):
- User story service implementations can run in parallel:
  - T009-T012 (Add Task)
  - T013-T014 (View Tasks)
  - T015-T017 (Toggle Complete)
- However, T018 (Update) and T020 (Delete) depend on T015 (get_task)

**Within Phase 11**:
- T036, T037, T038, T039 can all run in parallel (marked [P])

---

## Task Summary

| Phase | Tasks | Purpose |
|-------|-------|---------|
| 1 | T001-T002B | Project setup with Rich and pyfiglet |
| 2 | T003-T008 | Foundation (model + service skeleton) |
| 3 | T009-T012 | US1: Add Task |
| 4 | T013-T014 | US2: View Tasks |
| 5 | T015-T017 | US3: Toggle Complete |
| 6 | T018-T019 | US4: Update Task |
| 7 | T020-T021 | US5: Delete Task |
| 8 | T022-T026 | CLI Menu System with Rich UI and ASCII art |
| 9 | T027-T031 | CLI Action Handlers with Rich styling |
| 10 | T032-T034 | Main Loop with Rich Console |
| 11 | T035-T039 | Integration Tests |
| 12 | T040-T043 | Final Validation |

**Total Tasks**: 45 (added T002A, T002B, T022A)
**Estimated Checkpoints**: 12

**New UI Enhancements**:
- **ASCII Art**: pyfiglet for application header branding
- **Rich Library Features**:
  - Styled panels and tables for menu and task display
  - Color-coded messages (green for success, red for errors, yellow for warnings)
  - IntPrompt and Prompt.ask() for validated user input
  - Console clearing for better screen management
  - Box styling and formatted layouts
