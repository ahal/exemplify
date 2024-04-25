import os
import subprocess
from typing import Optional

from exemplify.steps.base import Step, register
from exemplify.util.process import run


@register()
class Npm(Step):
    name = "npm"

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

    @property
    def directive(self) -> str:
        return f"install {' '.join(self.packages)}"

    def exists(self) -> bool:
        try:
            run([self.npm, "show"] + self.packages)
            return True
        except subprocess.CalledProcessError:
            return False

    def sync(self) -> int:
        if self.exists():
            return run(self.args + ["--upgrade"] + self.packages).returncode
        return run(self.args + self.packages).returncode
