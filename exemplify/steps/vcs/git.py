from exemplify.steps.base import register
from exemplify.steps.vcs.base import VCS


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
