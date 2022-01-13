import os
import subprocess

from wellington.installables.base import Installable, register


@register("npm")
class Npm(Installable):
    def __init__(self, package, global_=True, npm_path=None):
        self.package = package
        npm_path = npm_path or "npm"
        self.npm = os.path.expanduser(npm_path)

        self.args = [self.npm, "install"]
        if global_:
            self.args.append("-g")

    def exists(self):
        try:
            subprocess.check_output([self.npm, "show", self.package])
            return True
        except subprocess.CalledProcessError:
            return False

    def install(self):
        subprocess.check_call(self.args + [self.package])

    def update(self):
        subprocess.check_call(self.args + ["--upgrade", self.package])

    def __str__(self):
        return "NPM INSTALL {}".format(self.package)
