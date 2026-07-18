#!/bin/bash
# run_test.sh — one command to run the whole test suite before deploying.
#
# Uses pytest (not `unittest discover`) on purpose: this repo has BOTH
# pytest-style tests (tests/test_routes.py) and unittest tests
# (tests/test_app.py, tests/test_db.py). pytest runs all of them; plain
# `unittest discover` would silently skip the pytest-style ones.
#
# conftest.py sets TESTING=true before importing the app, so the tests run
# against an in-memory SQLite database and never touch the real MySQL.

# Pick the project's virtualenv python if present, else fall back to PATH.
if [ -x "venv/bin/python" ]; then
    PY="venv/bin/python"            # VPS venv (see redeploy-site.sh)
elif [ -x ".venv/bin/python" ]; then
    PY=".venv/bin/python"           # local venv (macOS / Linux)
elif [ -x ".venv/Scripts/python.exe" ]; then
    PY=".venv/Scripts/python.exe"   # local venv (Windows / Git Bash)
else
    PY="python"                     # fall back to whatever is on PATH
fi

exec "$PY" -m pytest -v tests/
