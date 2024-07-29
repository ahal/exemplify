import os
import subprocess
import tempfile
from typing import Any, Generator, Optional

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

        self.alias = alias or f"{' && '.join(self.runcmds)} in {self.cwd}"

    @property
    def directive(self) -> str:
        return self.alias

    def exists(self) -> bool:
        if not self.checkcmd:
            return False

        return run(self.checkcmd, shell=True).returncode == 0

    def sync(self) -> Generator[str, str, int]:
        if self.exists():
            return 0

        returncode = 0
        for cmd in self.runcmds:
            yield f"+ {cmd.strip()}\n"
            proc = subprocess.Popen(
                cmd,
                cwd=self.cwd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

            assert proc.stdout
            for line in proc.stdout:
                yield line

            proc.wait()
            returncode |= proc.returncode

        return returncode
