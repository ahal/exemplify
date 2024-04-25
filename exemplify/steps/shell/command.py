import os
import tempfile
from typing import Optional

from exemplify.util.process import run
from exemplify.console import console
from exemplify.steps.base import Step, register


@register()
class Command(Step):
    name = "command"

    def __init__(
        self,
        meta: dict,
        run: list | str,
        check: Optional[str] = None,
        cwd: Optional[str] = None,
        alias: Optional[str] = None,
    ) -> None:
        self.runcmds = run

        if isinstance(self.runcmds, str):
            self.runcmds = [self.runcmds]

        self.checkcmd = check

        cwd = cwd or tempfile.mkdtemp()
        self.cwd = os.path.expanduser(cwd)
        if not os.path.isdir(self.cwd):
            os.makedirs(self.cwd)

        self.alias = alias or f"{' && '.join(self.runcmds)} in {self.cwd}"

    @property
    def directive(self) -> str:
        return self.alias

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
