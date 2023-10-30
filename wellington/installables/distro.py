import subprocess
from shutil import which

from wellington.installables.base import Installable, register


@register("dnf")
class Dnf(Installable):
    def __init__(self, meta, packages):
        self.packages = packages
        if isinstance(self.packages, str):
            self.packages = [self.packages]

    def exists(self):
        try:
            for package in self.packages:
                subprocess.check_call(["dnf", "list", "--installed", package])
            return True
        except subprocess.CalledProcessError:
            return False

    def install(self):
        subprocess.check_call(["sudo", "dnf", "install", "-y"] + self.packages)

    def update(self):
        subprocess.check_call(["sudo", "dnf", "upgrade", "-y"] + self.packages)

    def enabled(self):
        return bool(which("dnf"))

    def __str__(self):
        return "DNF INSTALL {}".format(" ".join(self.packages))


@register("apt")
class Apt(Installable):
    def __init__(self, meta, packages):
        self.packages = packages
        if isinstance(self.packages, str):
            self.packages = [self.packages]

    def exists(self):
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

    def install(self):
        subprocess.check_call(["sudo", "apt", "install", "-y"] + self.packages)

    def update(self):
        subprocess.check_call(["sudo", "apt", "upgrade", "-y"] + self.packages)

    def enabled(self):
        return bool(which("apt"))

    def __str__(self):
        return "DNF INSTALL {}".format(" ".join(self.packages))
