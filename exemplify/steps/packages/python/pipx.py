import os
import subprocess
from typing import Optional

from exemplify.steps.base import Step, register


@register("pipx")
class PipX(Step):
    def __init__(self, meta: dict, package: str, inject: Optional[str] = None) -> None:
        self.package = package
        self.inject = inject
        self.pipx = os.path.expanduser("~/.pyenv/shims/pipx")

    def exists(self) -> bool:
        try:
            output = subprocess.check_output(
                [self.pipx, "list", "--include-injected"], text=True
            )
            return self.package in output
        except subprocess.CalledProcessError:
            return False

    def sync(self) -> None:
        if self.exists():
            if self.inject:
                subprocess.check_call(
                    [self.pipx, "upgrade", "--include-injected", self.inject]
                )
            else:
                subprocess.check_call([self.pipx, "upgrade", self.package])
        else:
            if self.inject:
                subprocess.check_call([self.pipx, "inject", self.inject, self.package])
            else:
                subprocess.check_call([self.pipx, "install", self.package])

    def __str__(self):
        return "PIPX INSTALL {}".format(self.package)
