import os
import tempfile
from typing import Optional

from exemplify.util.process import run
from exemplify.console import console
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

    def exists(self) -> bool:
        if not self.checkcmd:
            return False

        return run(self.checkcmd, shell=True).returncode == 0

    def sync(self) -> int:
        if self.exists():
            return 0

        returncode = 0
        for cmd in self.runcmds:
            console.print(f"+ {cmd.strip()}")
            returncode |= run(cmd, shell=True).returncode

        return returncode

    def __str__(self):
        return f"RUN {' && '.join(self.runcmds)} in {self.cwd}"
