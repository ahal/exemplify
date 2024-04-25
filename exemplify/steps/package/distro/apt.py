import subprocess
from shutil import which

from exemplify.steps.base import Step, register
from exemplify.util.process import run


@register()
class Apt(Step):
    name = "apt"

    def __init__(self, meta: dict, packages: str | list[str]):
        if isinstance(packages, str):
            packages = [packages]
        self.packages = packages

    @property
    def directive(self) -> str:
        return f"install {' '.join(self.packages)}"

    def exists(self) -> bool:
        try:
            for package in self.packages:
                run(
                    ["dpkg", "-s", package],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT,
                )
            return True
        except subprocess.CalledProcessError:
            return False

    def sync(self) -> int:
        if self.exists():
            return run(["sudo", "apt", "upgrade", "-y"] + self.packages).returncode
        return run(["sudo", "apt", "install", "-y"] + self.packages).returncode

    def enabled(self) -> bool:
        return bool(which("apt"))
