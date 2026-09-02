"""Greeting generation module wrapper.

Re-exports the hello() function from the original src module.
This allows the fullstack backend to use the same greeting logic
as the original DTE demo module.
"""

from src.hello import hello

__all__ = ["hello"]
