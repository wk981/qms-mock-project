"""Greeting generation for the Hello Project.

Software Configuration Item: SCI-001

Implements:
    REQ-001 - Greeting: the greeting contains the supplied name.
    REQ-002 - Default Greeting: the greeting uses "Hello".
"""

DEFAULT_GREETING = "Hello"


def hello(name: str) -> str:
    """Return a greeting for ``name``.

    Args:
        name: The name to greet.

    Returns:
        A greeting of the form ``Hello, <name>``.
    """
    return f"{DEFAULT_GREETING}, {name}"
