from exemplify.steps.base import Step, register
from exemplify.util.process import run


@register("cargo")
class Cargo(Step):
    def __init__(self, meta: dict, packages: str | list[str]):
        if isinstance(packages, str):
            packages = [packages]
        self.packages = packages
        self.cargo = "cargo"

    def sync(self) -> int:
        proc = run([self.cargo, "install"] + self.packages)
        return proc.returncode

    def __str__(self):
        return f"CARGO INSTALL {', '.join(self.packages)}"
