import subprocess
from shutil import which

from exemplify.steps.base import Step, register
from exemplify.util.process import run


@register("dnf")
class Dnf(Step):
    def __init__(self, meta: dict, packages: str | list[str]) -> None:
        if isinstance(packages, str):
            packages = [packages]
        self.packages = packages

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

    def __str__(self):
        return "DNF INSTALL {}".format(" ".join(self.packages))
