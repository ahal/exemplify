import subprocess
from shutil import which

from dittoed.installables.base import Installable, register


@register("dnf")
class Dnf(Installable):
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

    def install(self) -> None:
        subprocess.check_call(["sudo", "dnf", "install", "-y"] + self.packages)

    def update(self) -> None:
        subprocess.check_call(["sudo", "dnf", "upgrade", "-y"] + self.packages)

    def enabled(self) -> bool:
        return bool(which("dnf"))

    def __str__(self):
        return "DNF INSTALL {}".format(" ".join(self.packages))


@register("apt")
class Apt(Installable):
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

    def install(self) -> None:
        subprocess.check_call(["sudo", "apt", "install", "-y"] + self.packages)

    def update(self) -> None:
        subprocess.check_call(["sudo", "apt", "upgrade", "-y"] + self.packages)

    def enabled(self) -> bool:
        return bool(which("apt"))

    def __str__(self):
        return "DNF INSTALL {}".format(" ".join(self.packages))
