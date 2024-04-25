import subprocess
from shutil import which

from exemplify.steps.base import Step, register
from exemplify.util.process import run


@register()
class Dnf(Step):
    name = "dnf"

    def __init__(self, meta: dict, packages: str | list[str]) -> None:
        if isinstance(packages, str):
            packages = [packages]
        self.packages = packages

    @property
    def directive(self) -> str:
        return f"install {' '.join(self.packages)}"

    def exists(self) -> bool:
        try:
            for package in self.packages:
                run(["dnf", "list", "--installed", package])
            return True
        except subprocess.CalledProcessError:
            return False

    def sync(self) -> int:
        if self.exists():
            return run(["sudo", "dnf", "upgrade", "-y"] + self.packages).returncode
        return run(["sudo", "dnf", "install", "-y"] + self.packages).returncode

    def enabled(self) -> bool:
        return bool(which("dnf"))
