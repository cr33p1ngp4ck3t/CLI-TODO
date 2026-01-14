# Quickstart: Phase I - In-Memory Todo Console Application

**Branch**: `001-phase1-todo-app` | **Date**: 2025-12-27

## Prerequisites

- Python 3.13 or higher
- UV package manager (optional, for dependency management)
- Terminal/console environment

## Project Setup

### 1. Clone and Navigate

```bash
cd "D:\Spec Driven Development\Hackathon II"
git checkout 001-phase1-todo-app
```

### 2. Create Project Structure

```bash
# Create source directories
mkdir -p src/models src/services src/cli

# Create test directories
mkdir -p tests/unit tests/integration

# Create __init__.py files for Python packages
touch src/__init__.py
touch src/models/__init__.py
touch src/services/__init__.py
touch src/cli/__init__.py
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py
```

### 3. Initialize UV Project (Optional)

```bash
# Initialize UV project
uv init

# Add pytest as dev dependency
uv add --dev pytest
```

If not using UV, create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install pytest
```

## Running the Application

### Start the Todo App

```bash
# With UV
uv run python -m src.main

# Without UV (after activating venv)
python -m src.main
```

### Expected Startup Output

```
=============================
       TODO APPLICATION
=============================

Main Menu:
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
6. Exit

Enter your choice (1-6): _
```

## Running Tests

### All Tests

```bash
# With UV
uv run pytest

# Without UV
pytest
```

### Unit Tests Only

```bash
uv run pytest tests/unit/
```

### Integration Tests Only

```bash
uv run pytest tests/integration/
```

### With Verbose Output

```bash
uv run pytest -v
```

### With Coverage (if installed)

```bash
uv add --dev pytest-cov
uv run pytest --cov=src --cov-report=term-missing
```

## Quick Verification

After implementation, verify the application works:

### Test 1: Add a Task

1. Select option `1` (Add Task)
2. Enter: `Buy groceries`
3. Verify: "Task 1 created successfully" message

### Test 2: View Tasks

1. Select option `2` (View Tasks)
2. Verify: Task 1 appears with description "Buy groceries"

### Test 3: Mark Complete

1. Select option `5` (Mark Complete/Incomplete)
2. Enter ID: `1`
3. Select option `2` (View Tasks)
4. Verify: Task 1 shows as complete (✓)

### Test 4: Exit

1. Select option `6` (Exit)
2. Verify: "Goodbye! Your tasks have not been saved." message
3. Verify: Application terminates

## File Structure Reference

After implementation, your project should have:

```
project-root/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py             # Task dataclass
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py     # Business logic
│   └── cli/
│       ├── __init__.py
│       └── menu.py             # Menu and user interaction
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_task.py
│   │   └── test_task_service.py
│   └── integration/
│       ├── __init__.py
│       └── test_cli.py
├── pyproject.toml              # UV/project configuration
└── specs/
    └── 001-phase1-todo-app/
        ├── spec.md
        ├── plan.md
        ├── research.md
        ├── data-model.md
        └── quickstart.md       # This file
```

## Troubleshooting

### "Module not found" Error

Ensure you're running from the project root and using `-m` flag:

```bash
# Correct
python -m src.main

# Incorrect
python src/main.py
```

### Python Version Error

Check your Python version:

```bash
python --version
# Should be 3.13.x or higher
```

### Tests Not Found

Ensure test files follow naming convention:

- Test files must start with `test_`
- Test functions must start with `test_`

## Next Steps

After completing Phase I:

1. Run `/sp.tasks` to generate implementation tasks
2. Follow tasks in dependency order
3. Ensure all acceptance tests pass
4. Review against spec.md success criteria
