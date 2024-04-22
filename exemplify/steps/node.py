import os
import subprocess
from typing import Optional

from exemplify.steps.base import Step, register


@register("npm")
class Npm(Step):
    def __init__(
        self,
        meta: dict,
        packages: str | list[str],
        global_: bool = True,
        npm_path: Optional[str] = None,
    ) -> None:
        if isinstance(packages, str):
            packages = [packages]
        self.packages = packages

        npm_path = npm_path or "npm"
        self.npm = os.path.expanduser(npm_path)

        self.args = [self.npm, "install"]
        if global_:
            self.args.append("-g")

    def exists(self) -> bool:
        try:
            subprocess.check_output([self.npm, "show"] + self.packages)
            return True
        except subprocess.CalledProcessError:
            return False

    def sync(self) -> None:
        if self.exists():
            subprocess.check_call(self.args + ["--upgrade"] + self.packages)
        else:
            subprocess.check_call(self.args + self.packages)

    def __str__(self):
        return "NPM INSTALL {}".format(" ".join(self.packages))
