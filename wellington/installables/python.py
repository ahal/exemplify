import os
import subprocess

from wellington.installables.base import Installable, register


@register("pip")
class Pip(Installable):
    def __init__(self, package, pip_path=None):
        self.package = package
        pip_path = pip_path or "~/.pyenv/shims/pip"
        self.pip = os.path.expanduser(pip_path)

    def exists(self):
        try:
            subprocess.check_output([self.pip, "show", self.package])
            return True
        except subprocess.CalledProcessError:
            return False

    def install(self):
        subprocess.check_call([self.pip, "install", self.package])

    def update(self):
        subprocess.check_call([self.pip, "install", "--upgrade", self.package])

    def __str__(self):
        return "PIP INSTALL {}".format(self.package)


@register("pipx")
class PipX(Installable):
    def __init__(self, package, inject=None):
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
        subprocess.check_call([self.pipx, "upgrade", self.package])

    def __str__(self):
        return "PIPX INSTALL {}".format(self.package)
