import os
import subprocess
from typing import Optional

from exemplify.steps.base import Step, register
from exemplify.util.process import run


@register("pipx")
class PipX(Step):
    def __init__(self, meta: dict, package: str, inject: Optional[str] = None) -> None:
        self.package = package
        self.inject = inject
        self.pipx = os.path.expanduser("~/.pyenv/shims/pipx")

    def exists(self) -> bool:
        try:
            output = run(
                [self.pipx, "list", "--include-injected"],
                capture_output=True,
                text=True,
            )
            return self.package in output
        except subprocess.CalledProcessError:
            return False

    def sync(self) -> int:
        if self.exists():
            if self.inject:
                return run(
                    [self.pipx, "upgrade", "--include-injected", self.inject],
                ).returncode
            return run([self.pipx, "upgrade", self.package]).returncode

        if self.inject:
            return run([self.pipx, "inject", self.inject, self.package]).returncode
        return run([self.pipx, "install", self.package]).returncode

    def __str__(self):
        return "PIPX INSTALL {}".format(self.package)
