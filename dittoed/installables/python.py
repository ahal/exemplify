import os
import subprocess
from typing import Optional

from dittoed.installables.base import Installable, register


@register("pip")
class Pip(Installable):
    def __init__(
        self, meta: dict, packages: str | list[str], pip_path: Optional[str] = None
    ) -> None:
        if isinstance(packages, str):
            packages = [packages]
        self.packages = packages

        pip_path = pip_path or "~/.pyenv/shims/pip"
        self.pip = os.path.expanduser(pip_path)

    def exists(self) -> bool:
        try:
            output = subprocess.check_output([self.pip, "list"], text=True)
            return all(p in output for p in self.packages)
        except subprocess.CalledProcessError:
            return False

    def install(self) -> None:
        subprocess.check_call([self.pip, "install"] + self.packages)

    def update(self) -> None:
        subprocess.check_call([self.pip, "install", "--upgrade"] + self.packages)

    def __str__(self):
        return f"PIP INSTALL {', '.join(self.packages)}"


@register("pipx")
class PipX(Installable):
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

    def install(self) -> None:
        if self.inject:
            subprocess.check_call([self.pipx, "inject", self.inject, self.package])
        else:
            subprocess.check_call([self.pipx, "install", self.package])

    def update(self) -> None:
        if self.inject:
            subprocess.check_call(
                [self.pipx, "upgrade", "--include-injected", self.inject]
            )
        else:
            subprocess.check_call([self.pipx, "upgrade", self.package])

    def __str__(self):
        return "PIPX INSTALL {}".format(self.package)
