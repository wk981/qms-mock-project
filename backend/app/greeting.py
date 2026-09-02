"""Greeting generation module."""

DEFAULT_GREETING = "Hello"


def hello(name: str) -> str:
    """Return a greeting for the given name.

    Args:
        name: The name to greet.

    Returns:
        A greeting of the form "Hello, <name>!".

    Raises:
        ValueError: If name is empty.
    """
    if not name:
        raise ValueError("Name cannot be empty")

    return f"{DEFAULT_GREETING}, {name}!"
