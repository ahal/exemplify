import os
from typing import Optional

from exemplify.steps.base import Step, register
from exemplify.util.process import run


@register()
class Pip(Step):
    name = "pip"

    def __init__(
        self, meta: dict, packages: str | list[str], pip_path: Optional[str] = None
    ) -> None:
        if isinstance(packages, str):
            packages = [packages]
        self.packages = packages

        pip_path = pip_path or "~/.pyenv/shims/pip"
        self.pip = os.path.expanduser(pip_path)

    @property
    def directive(self) -> str:
        return f"install {' '.join(self.packages)}"

    def sync(self) -> int:
        proc = run([self.pip, "install", "--upgrade"] + self.packages)
        return proc.returncode
