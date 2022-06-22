import subprocess

from wellington.installables.base import Installable, register


@register("cargo")
class Cargo(Installable):
    def __init__(self, meta, packages):
        self.packages = packages
        self.cargo = "cargo"

    def exists(self):
        try:
            output = subprocess.check_output(
                [self.cargo, "install", "--list"], text=True
            )
            return all(p in output for p in self.packages)
        except subprocess.CalledProcessError:
            return False

    def install(self):
        subprocess.check_call([self.cargo, "install"] + self.packages)

    def update(self):
        subprocess.check_call([self.cargo, "install"] + self.packages)

    def __str__(self):
        return f"CARGO INSTALL {', '.join(self.packages)}"
