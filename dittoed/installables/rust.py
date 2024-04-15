import subprocess

from dittoed.installables.base import Installable, register


@register("cargo")
class Cargo(Installable):
    def __init__(self, meta: dict, packages: str | list[str]):
        if isinstance(packages, str):
            packages = [packages]
        self.packages = packages
        self.cargo = "cargo"

    def sync(self) -> None:
        subprocess.check_call([self.cargo, "install"] + self.packages)

    def __str__(self):
        return f"CARGO INSTALL {', '.join(self.packages)}"
