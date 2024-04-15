import os
import shlex
import subprocess
import tempfile
from typing import Optional

from dittoed.installables.base import Installable, register


@register("command")
class Command(Installable):
    def __init__(
        self,
        meta: dict,
        run,
        check: Optional[str] = None,
        cwd: Optional[str] = None,
        shell: bool = False,
    ) -> None:
        self.runcmds = run

        if isinstance(self.runcmds, str):
            self.runcmds = [self.runcmds]

        self.checkcmd = check
        self.shell = shell

        cwd = cwd or tempfile.mkdtemp()
        self.cwd = os.path.expanduser(cwd)
        if not os.path.isdir(self.cwd):
            os.makedirs(self.cwd)

    def run(self, command: str) -> None:
        for cmd in command.split("&&"):
            print(f"+ {cmd}")
            if "|" not in cmd:
                if not self.shell:
                    cmd = shlex.split(cmd)
                    cmd[0] = os.path.expanduser(cmd[0])
                subprocess.check_call(cmd, cwd=self.cwd, shell=self.shell)
                continue

            proc = None
            for i, subcmd in enumerate(cmd.split("|")):
                if not self.shell:
                    subcmd = shlex.split(subcmd)
                    subcmd[0] = os.path.expanduser(subcmd[0])

                if i == 0:
                    proc = subprocess.Popen(
                        subcmd, stdout=subprocess.PIPE, cwd=self.cwd, shell=self.shell
                    )
                else:
                    assert proc
                    proc = subprocess.Popen(
                        subcmd,
                        stdout=subprocess.PIPE,
                        stdin=proc.stdout,
                        cwd=self.cwd,
                        shell=self.shell,
                    )

            assert proc
            output = proc.communicate()[0]
            print(output)
            if proc.returncode:
                raise subprocess.CalledProcessError(
                    returncode=proc.returncode, cmd=cmd, output=output
                )

    def exists(self) -> bool:
        if not self.checkcmd:
            return False

        try:
            self.run(self.checkcmd)
            return True
        except subprocess.CalledProcessError:
            return False

    def install(self) -> None:
        for cmd in self.runcmds:
            self.run(cmd)

    def __str__(self):
        return f"RUN {' && '.join(self.runcmds)} in {self.cwd}"
