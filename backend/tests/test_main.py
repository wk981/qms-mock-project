"""API tests for the FastAPI greeting service."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_greet_success():
    """POST /api/greet returns a greeting for a valid name."""
    response = client.post("/api/greet", json={"name": "Alice"})
    assert response.status_code == 200
    data = response.json()
    assert "greeting" in data
    assert "Alice" in data["greeting"]
    assert data["greeting"].startswith("Hello")
    assert data["greeting"].endswith("!")


def test_greet_empty_name():
    """POST /api/greet returns 400 for an empty name."""
    response = client.post("/api/greet", json={"name": ""})
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data


def test_health_check():
    """GET /health returns status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
