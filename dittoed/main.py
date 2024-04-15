import os
from typing import Optional

import tomli

from dittoed.installables.base import Installable, registry
from dittoed.util.merge import merge


def install(item: Installable) -> None:
    if not item.enabled():
        return
    if item.exists():
        return
    print("####")
    print(item)
    print("####")
    item.install()


def update(item: Installable) -> None:
    if not item.enabled():
        return
    print("####")
    print(item)
    print("####")
    if item.exists():
        item.update()
    else:
        item.install()


def parse_config(path: str) -> dict:
    root_path = os.path.dirname(path)

    with open(path, "rb") as fh:
        data = tomli.load(fh)

    data.setdefault("meta", {})
    for item in data["meta"].pop("include", []):
        path = os.path.join(root_path, f"{item}.toml")
        data = merge(parse_config(path), data)

    data["meta"]["root"] = root_path
    return data


def generate_installables(config: dict, routines: Optional[list[str]] = None):
    g_meta = config.pop("meta", {})
    routines = routines or g_meta.get("defaults", config.keys())
    for name in routines:
        pmsg = f"\nPROCESSING ROUTINE {name}"
        print(pmsg)
        print("-" * len(pmsg))
        meta = config[name].pop("meta", None)
        steps = config[name]["step"]
        for step in steps:
            i_type = step.pop("type")

            # Interpolate meta data into step values.
            if meta:
                for key, val in step.items():
                    step[key] = val.format(**meta)

            installable = registry[i_type](g_meta, **step)
            yield installable
