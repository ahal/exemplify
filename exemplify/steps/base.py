import os
from abc import ABC, abstractmethod
from typing import Callable

from exemplify.util.python_path import import_modules


registry = {}


def register(name: str) -> Callable:
    def wrap(cls):
        if name not in registry:
            registry[name] = cls

    return wrap


class Step(ABC):
    @abstractmethod
    def sync(self) -> int:
        pass

    def enabled(self) -> bool:
        return True


# Trigger step registration.
import_modules(exceptions=os.path.basename(__file__))
