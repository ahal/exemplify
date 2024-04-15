import subprocess

from dittoed.installables.base import Installable, register


@register("cargo")
class Cargo(Installable):
    def __init__(self, meta: dict, packages: str | list[str]):
        if isinstance(packages, str):
            packages = [packages]
        self.packages = packages
        self.cargo = "cargo"

    def exists(self) -> bool:
        try:
            output = subprocess.check_output(
                [self.cargo, "install", "--list"], text=True
            )
            return all(p in output for p in self.packages)
        except subprocess.CalledProcessError:
            return False

    def install(self) -> None:
        subprocess.check_call([self.cargo, "install"] + self.packages)

    def update(self) -> None:
        subprocess.check_call([self.cargo, "install"] + self.packages)

    def __str__(self):
        return f"CARGO INSTALL {', '.join(self.packages)}"
