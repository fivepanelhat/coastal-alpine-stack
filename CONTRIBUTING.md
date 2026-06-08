# Contributing to Coastal Alpine Stack

Thank you for contributing to the Coastal Alpine Stack! To ensure professional presentation and reliability across our edge platforms, please follow these guidelines.

## Code Standards & Style

We use strict Python style and type checkers to enforce code quality.

1. **Code Formatting:** We use **Black** with default settings.
   ```bash
   black .
   ```
2. **Type Checking:** All public interfaces must include type hints. We validate using **mypy**.
   ```bash
   mypy .
   ```
3. **Docstrings:** All modules, classes, and public functions must have docstrings describing their intent, parameters, and return types.
4. **Telemetry:** When calling external runtimes (like Ollama or OpenCV inference), use the `coastal_alpine_core.telemetry` helpers to log latency, tokens per second, and performance flags.

## Development Setup

1. Clone the stack and set up a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
2. Install the shared core in editable mode:
   ```bash
   pip install -e ./coastal_alpine_core
   ```
3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
4. Run tests before submitting changes:
   ```bash
   pytest
   ```

## Workflow & Releases
- Follow **Semantic Versioning** (MAJOR.MINOR.PATCH) for tags and package definitions.
- Document changes in `CHANGELOG.md` inside the modified sub-repository, and update the root `CHANGELOG.md` upon releases.
- Always include environment variable configurations in `.env.example` when adding a configuration dependency.
