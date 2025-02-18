import os
import tempfile
from typing import Any, Optional

from rich.console import RenderableType
from rich.syntax import Syntax

from exemplify.steps.base import Step, register
from exemplify.util.process import run


@register()
class Command(Step):
    name = "command"

    def __init__(
        self,
        meta: dict[str, Any],
        run: list | str,
        check: Optional[str] = None,
        cwd: Optional[str] = None,
        alias: Optional[str] = None,
    ) -> None:
        super().__init__(meta)

        self.runcmds = run

        if isinstance(self.runcmds, str):
            self.runcmds = [self.runcmds]

        self.checkcmd = check

        cwd = cwd or tempfile.mkdtemp()
        self.cwd = os.path.expanduser(cwd)
        if not os.path.isdir(self.cwd):
            os.makedirs(self.cwd)

        self.alias = alias or f"{' && '.join(self.runcmds)}"

    @property
    def directive(self) -> RenderableType:
        return Syntax(self.alias, "shell", background_color="default")

    def exists(self) -> bool:
        if not self.checkcmd:
            return False

        return run(self.checkcmd, shell=True).returncode == 0

    def sync(self) -> int:
        if self.exists():
            return 0

        returncode = 0
        for cmd in self.runcmds:
            proc = run(
                cmd,
                cwd=self.cwd,
                shell=True,
                text=True,
            )
            returncode |= proc.returncode

        return returncode
