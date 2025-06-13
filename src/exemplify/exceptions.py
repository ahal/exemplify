"""
Custom exceptions for exemplify.
"""


class ProjectNotFound(Exception):
    """Raised when a `ProjectStep` is used from outside the context of a
    repository."""
