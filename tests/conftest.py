"""Shared pytest fixtures for the Flask app tests."""
import os
import sys

import pytest

# Make the project root importable so `from app import app` works from anywhere.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Run the whole test suite against an in-memory SQLite DB, never the real MySQL.
# MUST be set BEFORE importing app, because app opens its DB connection at import
# time. (No-op until app has the TESTING->SQLite switch; harmless before then.)
os.environ["TESTING"] = "true"

from app import app as flask_app  # noqa: E402


@pytest.fixture
def client():
    flask_app.config.update(TESTING=True)
    with flask_app.test_client() as c:
        yield c
