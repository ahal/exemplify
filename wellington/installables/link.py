import os
import subprocess

from wellington.installables.base import Installable, register


@register("link")
class Link(Installable):
    def __init__(self, meta, source, dest=None, name=None):
        self.source = os.path.expanduser(source)
        if not os.path.isabs(self.source):
            self.source = os.path.join(meta["root"], source)

        self.name = name
        dest = dest or "~"
        dest = os.path.expanduser(dest)
        if os.path.isdir(dest):
            self.dest = dest
            if not self.name:
                self.name = os.path.basename(source)
        else:
            self.dest, self.name = os.path.split(dest)
        self.path = os.path.join(self.dest, self.name)

    def exists(self):
        if os.path.lexists(self.path):
            os.remove(self.path)
        return False

    def install(self):
        if not os.path.isdir(self.dest):
            os.makedirs(self.dest)

        subprocess.check_call(["ln", "-s", self.source, self.name], cwd=self.dest)

    def __str__(self):
        return "LINK {} to {}".format(self.source, self.path)

