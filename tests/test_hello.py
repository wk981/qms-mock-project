"""Unit tests for SCI-001 (src/hello.py).

Each test verifies one requirement from docs/requirements.md.
"""

import pytest

from src.hello import hello


def test_greeting_contains_name():
    """REQ-001: the greeting contains the supplied name."""
    assert "Alice" in hello("Alice")


def test_default_greeting():
    """REQ-002: the greeting uses "Hello" as the default greeting."""
    assert hello("Alice").startswith("Hello")


def test_empty_name_is_rejected():
    """REQ-003: an empty name is rejected with a ValueError."""
    with pytest.raises(ValueError):
        hello("")


def test_greeting_ends_with_exclamation_mark():
    """REQ-004: the greeting ends with an exclamation mark."""
    assert hello("Alice").endswith("!")
