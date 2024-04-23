import os
import subprocess
from typing import Optional

from exemplify.steps.base import Step, register


@register("link")
class Link(Step):
    def __init__(
        self,
        meta: dict,
        source: str,
        dest: Optional[str] = None,
        name: Optional[str] = None,
    ) -> None:
        self.source = os.path.expanduser(source)
        if not os.path.isabs(self.source):
            self.source = os.path.join(meta["root"], source)

        dest = dest or "~"
        dest = os.path.expanduser(dest)
        if os.path.isdir(dest):
            self.dest = dest
            if not name:
                self.name = os.path.basename(source)
            else:
                self.name = name
        else:
            self.dest, self.name = os.path.split(dest)
        self.path = os.path.join(self.dest, self.name)

    def sync(self) -> None:
        if os.path.lexists(self.path):
            os.remove(self.path)

        if not os.path.isdir(self.dest):
            os.makedirs(self.dest)

        subprocess.check_call(["ln", "-s", self.source, self.name], cwd=self.dest)

    def __str__(self):
        return "LINK {} to {}".format(self.source, self.path)
