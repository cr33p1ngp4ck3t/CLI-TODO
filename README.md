# Evolution of Todo - Phase I

A simple, menu-driven Python console application for managing todo tasks with in-memory storage.

## Features

-   Add new tasks
-   Update task descriptions
-   Delete tasks
-   Mark tasks as complete/incomplete
-   Beautiful CLI with Rich library styling
-   ASCII art header with pyfiglet

## Requirements

-   Python 3.13 or higher
-   UV package manager (recommended) or pip

## Installation

### Using UV (Recommended)

```bash
# Clone the repository
git https://github.com/cr33p1ngp4ck3t/CLI-TODO

# Install dependencies
uv sync
```

### Using pip

```bash
# Activate virtual environment
.venv\Scripts\activate  # On Windows
# source .venv/bin/activate  # On Linux/Mac

# Install dev dependencies
pip install -e ".[dev]"
```

## Running the Application

### With UV

```bash
uv run python -m src.main
```

### With pip

```bash
python -m src.main
```

## Running Tests

```bash
# All tests
uv run pytest

# Unit tests only
uv run pytest tests/unit/

# Integration tests only
uv run pytest tests/integration/

# With coverage report
uv run pytest --cov=src --cov-report=term-missing
```

## Usage

The application presents a menu-driven interface:

1. **Add Task** - Create a new todo item
2. **View Tasks** - Display all tasks with their status
3. **Update Task** - Modify an existing task description
4. **Delete Task** - Remove a task permanently
5. **Mark Complete/Incomplete** - Toggle task completion status
6. **Exit** - Close the application

## Project Structure

```
.
├── src/
│   ├── models/
│   │   └── task.py          # Task entity
│   ├── services/
│   │   └── task_service.py  # Business logic
│   ├── cli/
│   │   └── menu.py          # CLI interface
│   └── main.py              # Application entry point
├── tests/
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── specs/                   # Specification documents
└── pyproject.toml           # Project configuration
```

## Phase I Specifications

This is Phase I of the "Evolution of Todo" project. The implementation:

-   Uses **in-memory storage only** (no persistence)
-   Has **no external dependencies** beyond Rich and pyfiglet
-   Follows **clean architecture** principles
-   Implements **all basic CRUD operations**
-   Includes comprehensive test coverage

For complete specifications, see: `specs/001-phase1-todo-app/spec.md`

## Test Coverage

-   **34 tests** (27 unit + 7 integration)
-   **100% coverage** on service layer
-   All acceptance criteria validated

## Next Steps

Phase II will add:

-   Full-stack web application (Next.js + FastAPI)
-   Persistent storage (Neon PostgreSQL)
-   User authentication (Better Auth)
-   RESTful API

## License

This is an educational project demonstrating Spec-Driven Development methodology.

