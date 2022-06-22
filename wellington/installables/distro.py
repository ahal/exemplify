import subprocess

from wellington.installables.base import Installable, register


DISTRO = None
with open("/etc/os-release") as fh:
    for line in fh.readlines():
        line = line.strip()
        k, v = line.split("=")
        if k == "ID":
            DISTRO = v
            break


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
        return DISTRO == "fedora"

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
        return DISTRO == "ubuntu"

    def __str__(self):
        return "DNF INSTALL {}".format(" ".join(self.packages))
