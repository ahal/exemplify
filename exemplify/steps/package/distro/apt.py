import subprocess
from shutil import which

from exemplify.steps.base import Step, register
from exemplify.util.process import run


@register("apt")
class Apt(Step):
    def __init__(self, meta: dict, packages: str | list[str]):
        if isinstance(packages, str):
            packages = [packages]
        self.packages = packages

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

    def sync(self) -> None:
        if self.exists():
            run(["sudo", "apt", "upgrade", "-y"] + self.packages)
        else:
            run(["sudo", "apt", "install", "-y"] + self.packages)

    def enabled(self) -> bool:
        return bool(which("apt"))

    def __str__(self):
        return "APT INSTALL {}".format(" ".join(self.packages))
