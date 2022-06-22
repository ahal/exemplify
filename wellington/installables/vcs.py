import os
import subprocess
from abc import ABC, abstractproperty
from typing import List

from wellington.installables.base import Installable, register


class VCS(Installable, ABC):

    @abstractproperty
    def install_command(self) -> List[str]:
        ...

    @abstractproperty
    def update_command(self) -> List[str]:
        ...

    def __init__(self, meta, repo, dest, name=None):
        self.repo = repo
        self.dest = os.path.expanduser(dest)
        self.name = name

        name = self.name or self.repo.rstrip("/").rsplit("/", 1)[1]
        self.path = os.path.join(self.dest, name)

    def exists(self):
        return os.path.isdir(self.path)

    def install(self):
        if not os.path.isdir(self.dest):
            os.makedirs(self.dest)
        cmd = self.install_command[:]
        cmd.append(self.repo)

        if self.name:
            cmd.append(self.name)

        subprocess.check_call(cmd, cwd=self.dest)

    def update(self):
        subprocess.check_call(self.update_command, cwd=self.path)

    def __str__(self):
        return "PULL {} to {}".format(self.repo, self.path)


@register("hg")
class Mercurial(VCS):
    install_command = ["hg", "clone"]
    update_command = ["hg", "pull", "--update"]


@register("git")
class Git(VCS):
    install_command = ["git", "clone"]

    def __init__(self, *args, **kwargs):
        self.branch = kwargs.pop("branch", "main")
        super().__init__(*args, **kwargs)

    @property
    def update_command(self):
        return ["git", "pull", "origin", self.branch]

