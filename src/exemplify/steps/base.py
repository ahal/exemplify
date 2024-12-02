import os
from abc import ABC, abstractmethod
from typing import Any, Callable, Generator

from rich.console import RenderableType

from exemplify.main import console
from exemplify.util.python_path import import_modules


registry = {}


def register() -> Callable:
    def wrap(cls):
        if cls.name not in registry:
            registry[cls.name] = cls

    return wrap


class Step(ABC):
    name: str = ""

    def __init__(self, meta: dict[str, Any]) -> None:
        self.meta = meta

    @property
    @abstractmethod
    def directive(self) -> RenderableType: ...

    @abstractmethod
    def sync(self) -> int | Generator[str, str, int]: ...

    def enabled(self) -> bool:
        return True

    def __str__(self):
        with console.capture() as capture:
            console.print(f"[blue]{self.name.upper()}[/blue] ", end="")
            console.print(self.directive, end="")
        return capture.get().strip()


# Trigger step registration.
import_modules(exceptions=os.path.basename(__file__))
