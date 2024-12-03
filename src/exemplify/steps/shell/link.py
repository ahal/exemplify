import os
from typing import Optional

from exemplify.util.process import run
from exemplify.steps.base import Step, register


@register()
class Link(Step):
    name = "link"

    def __init__(
        self,
        meta: dict,
        source: str,
        dest: Optional[str] = None,
        basename: Optional[str] = None,
    ) -> None:
        super().__init__(meta)

        self.source = os.path.expanduser(source)
        if not os.path.isabs(self.source):
            self.source = os.path.join(self.meta["root"], source)

        dest = dest or "~"
        dest = os.path.expanduser(dest)
        if os.path.isdir(dest):
            self.dest = dest
            if not basename:
                self.basename = os.path.basename(source)
            else:
                self.basename = basename
        else:
            self.dest, self.basename = os.path.split(dest)
        self.path = os.path.join(self.dest, self.basename)

    @property
    def directive(self) -> str:
        return "{} to {}".format(self.source, self.path)

    def sync(self) -> int:
        if os.path.lexists(self.path):
            os.remove(self.path)

        if not os.path.isdir(self.dest):
            os.makedirs(self.dest)

        return run(["ln", "-s", self.source, self.basename], cwd=self.dest).returncode
