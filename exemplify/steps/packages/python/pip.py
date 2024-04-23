import os
import subprocess
from typing import Optional

from exemplify.steps.base import Step, register


@register("pip")
class Pip(Step):
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

    def sync(self) -> None:
        args = [self.pip, "install"]
        if self.exists():
            args.append("--upgrade")
        subprocess.check_call(args + self.packages)

    def __str__(self):
        return f"PIP INSTALL {', '.join(self.packages)}"
