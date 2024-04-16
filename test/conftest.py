from dittoed.installables.base import Installable


class FakeInstallable(Installable):
    def __init__(self, meta: dict, key) -> None:
        self.key = key

    def sync(self, *args, **kwargs):
        pass
