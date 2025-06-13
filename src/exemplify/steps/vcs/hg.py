"""
Mercurial version control management step.
"""
from exemplify.steps.base import register
from exemplify.steps.vcs.base import VCS


@register()
class Mercurial(VCS):
    name = "hg"

    @property
    def install_command(self) -> list[str]:
        return ["hg", "clone"]

    @property
    def update_command(self) -> list[str]:
        return ["hg", "pull", "--update"]
