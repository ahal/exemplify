import os
from abc import ABC, abstractmethod
from typing import Callable

from exemplify.util.python_path import import_modules


registry = {}


def register() -> Callable:
    def wrap(cls):
        if cls.name not in registry:
            registry[cls.name] = cls

    return wrap


class Step(ABC):
    name: str = ""

    @property
    @abstractmethod
    def directive(self) -> str: ...

    @abstractmethod
    def sync(self) -> int: ...

    def enabled(self) -> bool:
        return True

    def __str__(self):
        return f"{self.name.upper()}: {self.directive}"


# Trigger step registration.
import_modules(exceptions=os.path.basename(__file__))
