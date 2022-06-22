import os
import subprocess

from wellington.installables.base import Installable, register


@register("npm")
class Npm(Installable):
    def __init__(self, meta, packages, global_=True, npm_path=None):
        self.packages = packages
        if isinstance(self.packages, str):
            self.packages = [self.packages]

        npm_path = npm_path or "npm"
        self.npm = os.path.expanduser(npm_path)

        self.args = [self.npm, "install"]
        if global_:
            self.args.append("-g")

    def exists(self):
        try:
            subprocess.check_output([self.npm, "show"] + self.packages)
            return True
        except subprocess.CalledProcessError:
            return False

    def install(self):
        subprocess.check_call(self.args + self.packages)

    def update(self):
        subprocess.check_call(self.args + ["--upgrade"] + self.packages)

    def __str__(self):
        return "NPM INSTALL {}".format(" ".join(self.packages))
