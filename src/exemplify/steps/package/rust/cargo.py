"""
Rust Cargo package management step.
"""
from typing import List

from exemplify.steps.base import Step, register
from exemplify.util.process import run


@register()
class Cargo(Step):
    name = "cargo"

    def __init__(self, meta: dict[str, Any], packages: str | List[str]) -> None:
        super().__init__(meta)

        if isinstance(packages, str):
            packages = [packages]
        self.packages = packages
        self.cargo = "cargo"

    @property
    def directive(self) -> str:
        return f"install {' '.join(self.packages)}"

    def sync(self) -> int:
        proc = run([self.cargo, "install"] + self.packages)
        return proc.returncode
