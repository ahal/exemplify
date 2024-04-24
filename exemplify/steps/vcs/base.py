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
        self, meta: dict, repo: str, dest: str, name: Optional[str] = None
    ) -> None:
        self.repo = repo
        self.dest = os.path.expanduser(dest)
        self.name = name

        name = self.name or self.repo.rstrip("/").rsplit("/", 1)[1]
        self.path = os.path.join(self.dest, name)

    def exists(self) -> bool:
        return os.path.isdir(self.path)

    def sync(self) -> None:
        if self.exists():
            run(self.update_command, cwd=self.path)
            return

        if not os.path.isdir(self.dest):
            os.makedirs(self.dest)
        cmd = self.install_command[:]
        cmd.append(self.repo)

        if self.name:
            cmd.append(self.name)

        run(cmd, cwd=self.dest)

    def __str__(self):
        return "PULL {} to {}".format(self.repo, self.path)
