"""Unit tests for the greeting module."""

import pytest

from app.greeting import hello


def test_greeting_contains_name():
    """The greeting contains the supplied name."""
    assert "Alice" in hello("Alice")


def test_default_greeting():
    """The greeting uses 'Hello' as the default greeting."""
    assert hello("Alice").startswith("Hello")


def test_empty_name_is_rejected():
    """An empty name is rejected with a ValueError."""
    with pytest.raises(ValueError):
        hello("")


def test_greeting_ends_with_exclamation_mark():
    """The greeting ends with an exclamation mark."""
    assert hello("Alice").endswith("!")
