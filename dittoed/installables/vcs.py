import os
import subprocess
from abc import ABC, abstractmethod
from typing import Optional

from dittoed.installables.base import Installable, register


class VCS(Installable, ABC):
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

    def install(self) -> None:
        if not os.path.isdir(self.dest):
            os.makedirs(self.dest)
        cmd = self.install_command[:]
        cmd.append(self.repo)

        if self.name:
            cmd.append(self.name)

        subprocess.check_call(cmd, cwd=self.dest)

    def update(self) -> None:
        subprocess.check_call(self.update_command, cwd=self.path)

    def __str__(self):
        return "PULL {} to {}".format(self.repo, self.path)


@register("hg")
class Mercurial(VCS):
    @property
    def install_command(self):
        return ["hg", "clone"]

    @property
    def update_command(self):
        return ["hg", "pull", "--update"]


@register("git")
class Git(VCS):
    def __init__(self, *args, **kwargs) -> None:
        self.branch = kwargs.pop("branch", "main")
        super().__init__(*args, **kwargs)

    @property
    def install_command(self):
        return ["git", "clone"]

    @property
    def update_command(self):
        return ["git", "pull", "origin", self.branch]
