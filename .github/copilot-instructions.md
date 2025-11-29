# Copilot Instructions for python-course-assignments

Repository: `python-course-assignments`

Purpose
- Help contributors and the assistant produce small, self-contained Python exercises and fixes for an educational repo of short assignments.

Context
- The repo contains daily Python exercises under `day01/`, `day02/`, etc., and a small project in `day04/project/`.
- Tests are present (e.g., `test_pcr_calculator.py`). Keep changes small and focused so tests remain runnable.

When responding
- Prefer minimal, focused edits. Explain changes briefly (1–3 sentences) when producing patches.
- Always favor clarity and readability over cleverness.
- Run or suggest unit tests when you modify code; include exact commands to run tests using `pytest` if available.

Style & constraints
- Follow idiomatic Python and PEP 8 styling unless existing code intentionally deviates.
- Do not add heavy external dependencies. If a dependency is necessary, note it explicitly and add it to `requirements.txt` or `pyproject.toml`.
- Keep functions small and well-named. Avoid global state changes unless required.

Files to focus on
- For day exercises, prioritize the `dayNN/*.py` files and their corresponding `test_*.py` tests.
- For the `day04/project/` app, review `project/main.py`, `project/config.py`, and modules under `business_logic/` and `ui/`.

Testing
- Prefer running tests locally using the project test runner. Example commands:
  - `pip install -r day04/project/requirements.txt` (if present)
  - `pytest -q`

What NOT to do
- Do not rewrite large portions of the repository without an explicit request.
- Do not remove or silence tests; prefer fixing failing tests with minimal, correct changes.

Example assistant behavior
- When asked to fix a failing test: run the tests, identify the failing assertion, propose a minimal patch, and update tests only if the test is wrong.
- When asked to add a feature: open a brief plan, implement the smallest runnable change, and add/modify tests demonstrating the feature.

Contact / notes
- Keep commits and changes atomic and well-described. When in doubt, ask the maintainer for clarification.
