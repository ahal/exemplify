import os
from abc import ABC, abstractmethod
from typing import Optional

from exemplify.util.process import run
from exemplify.steps.base import Step


class VCS(Step, ABC):
    @property
    @abstractmethod
    def install_command(self) -> list[str]: ...

    @property
    @abstractmethod
    def update_command(self) -> list[str]: ...

    def __init__(
        self, meta: dict, repo: str, dest: str, basename: Optional[str] = None
    ) -> None:
        super().__init__(meta)

        self.repo = repo
        self.dest = os.path.expanduser(dest)
        self.basename = basename

        basename = self.basename or self.repo.rstrip("/").rsplit("/", 1)[1]
        self.path = os.path.join(self.dest, basename)

    def exists(self) -> bool:
        return os.path.isdir(self.path)

    @property
    def directive(self):
        verb = "pull" if self.exists() else "clone"
        return f"{verb} {self.repo} to {self.path}"

    def sync(self) -> int:
        if self.exists():
            return run(self.update_command, cwd=self.path).returncode

        if not os.path.isdir(self.dest):
            os.makedirs(self.dest)
        cmd = self.install_command[:]
        cmd.append(self.repo)

        if self.basename:
            cmd.append(self.name)

        return run(cmd, cwd=self.dest).returncode
