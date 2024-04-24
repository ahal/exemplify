import os
import subprocess
import tempfile
from typing import Optional

from exemplify.steps.base import Step, register


@register("command")
class Command(Step):
    def __init__(
        self,
        meta: dict,
        run: list | str,
        check: Optional[str] = None,
        cwd: Optional[str] = None,
    ) -> None:
        self.runcmds = run

        if isinstance(self.runcmds, str):
            self.runcmds = [self.runcmds]

        self.checkcmd = check

        cwd = cwd or tempfile.mkdtemp()
        self.cwd = os.path.expanduser(cwd)
        if not os.path.isdir(self.cwd):
            os.makedirs(self.cwd)

    def run(self, cmd: str) -> None:
        print(f"+ {cmd.strip()}")
        subprocess.run(cmd, check=True, shell=True)

    def exists(self) -> bool:
        if not self.checkcmd:
            return False

        try:
            self.run(self.checkcmd)
            return True
        except subprocess.CalledProcessError:
            return False

    def sync(self) -> None:
        if self.exists():
            return

        for cmd in self.runcmds:
            self.run(cmd)

    def __str__(self):
        return f"RUN {' && '.join(self.runcmds)} in {self.cwd}"
