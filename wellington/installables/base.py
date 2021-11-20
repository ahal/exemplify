import os
from abc import ABC, abstractmethod

from wellington.util.python_path import import_sibling_modules


registry = {}

def register(name):

    def wrap(cls):
        if name not in registry:
            registry[name] = cls

    return wrap


class Installable(ABC):

    @abstractmethod
    def exists(self):
        pass

    @abstractmethod
    def install(self):
        pass

    def update(self):
        print("Update not implemented")

    def enabled(self):
        return True


# Trigger installable registration.
import_sibling_modules(exceptions=os.path.basename(__file__))
