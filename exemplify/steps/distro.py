import subprocess
from shutil import which

from exemplify.steps.base import Step, register


@register("dnf")
class Dnf(Step):
    def __init__(self, meta: dict, packages: str | list[str]) -> None:
        if isinstance(packages, str):
            packages = [packages]
        self.packages = packages

    def exists(self) -> bool:
        try:
            for package in self.packages:
                subprocess.check_call(["dnf", "list", "--installed", package])
            return True
        except subprocess.CalledProcessError:
            return False

    def sync(self) -> None:
        if self.exists():
            subprocess.check_call(["sudo", "dnf", "upgrade", "-y"] + self.packages)
        else:
            subprocess.check_call(["sudo", "dnf", "install", "-y"] + self.packages)

    def enabled(self) -> bool:
        return bool(which("dnf"))

    def __str__(self):
        return "DNF INSTALL {}".format(" ".join(self.packages))


@register("apt")
class Apt(Step):
    def __init__(self, meta: dict, packages: str | list[str]):
        if isinstance(packages, str):
            packages = [packages]
        self.packages = packages

    def exists(self) -> bool:
        try:
            for package in self.packages:
                subprocess.check_call(
                    ["dpkg", "-s", package],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT,
                )
            return True
        except subprocess.CalledProcessError:
            return False

    def sync(self) -> None:
        if self.exists():
            subprocess.check_call(["sudo", "apt", "upgrade", "-y"] + self.packages)
        else:
            subprocess.check_call(["sudo", "apt", "install", "-y"] + self.packages)

    def enabled(self) -> bool:
        return bool(which("apt"))

    def __str__(self):
        return "APT INSTALL {}".format(" ".join(self.packages))
