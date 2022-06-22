import os
import subprocess

from wellington.installables.base import Installable, register


@register("pip")
class Pip(Installable):
    def __init__(self, meta, packages, pip_path=None):
        self.packages = packages

        if isinstance(self.packages, str):
            self.packages = [self.packages]

        pip_path = pip_path or "~/.pyenv/shims/pip"
        self.pip = os.path.expanduser(pip_path)

    def exists(self):
        try:
            output = subprocess.check_output([self.pip, "list"], text=True)
            return all(p in output for p in self.packages)
        except subprocess.CalledProcessError:
            return False

    def install(self):
        subprocess.check_call([self.pip, "install"] + self.packages)

    def update(self):
        subprocess.check_call([self.pip, "install", "--upgrade"] + self.packages)

    def __str__(self):
        return f"PIP INSTALL {', '.join(self.packages)}"


@register("pipx")
class PipX(Installable):
    def __init__(self, meta, package, inject=None):
        self.package = package
        self.inject = inject
        self.pipx = os.path.expanduser("~/.pyenv/shims/pipx")

    def exists(self):
        try:
            output = subprocess.check_output(
                [self.pipx, "list", "--include-injected"], text=True
            )
            return self.package in output
        except subprocess.CalledProcessError:
            return False

    def install(self):
        if self.inject:
            subprocess.check_call([self.pipx, "inject", self.inject, self.package])
        else:
            subprocess.check_call([self.pipx, "install", self.package])

    def update(self):
        if self.inject:
            subprocess.check_call([self.pipx, "upgrade", "--include-injected", self.inject])
        else:
            subprocess.check_call([self.pipx, "upgrade", self.package])

    def __str__(self):
        return "PIPX INSTALL {}".format(self.package)
