from exemplify.steps.base import register
from exemplify.steps.vcs.base import VCS


@register("hg")
class Mercurial(VCS):
    @property
    def install_command(self):
        return ["hg", "clone"]

    @property
    def update_command(self):
        return ["hg", "pull", "--update"]
