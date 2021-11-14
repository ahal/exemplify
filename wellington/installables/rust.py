import subprocess

from wellington.installables.base import Installable, register


@register("cargo")
class Cargo(Installable):
    def __init__(self, package):
        self.package = package
        self.cargo = "cargo"

    def exists(self):
        try:
            output = subprocess.check_output(
                [self.cargo, "install", "--list"], text=True
            )
            return self.package in output
        except subprocess.CalledProcessError:
            return False

    def install(self):
        subprocess.check_call([self.cargo, "install", self.package])

    def update(self):
        subprocess.check_call([self.cargo, "install", self.package])

    def __str__(self):
        return "CARGO INSTALL {}".format(self.package)
