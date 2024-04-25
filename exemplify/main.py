import os
from typing import Optional

import tomli

from exemplify.console import console
from exemplify.steps.base import Step, registry
from exemplify.util.merge import merge


def synchronize(item: Step) -> None:
    if not item.enabled():
        return

    console.print(item)
    with console.capture() as capture:
        ret = item.sync()

    if ret != 0:
        print("FOOBAR")
        print(capture.get())


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


def generate_steps(config: dict, routines: Optional[list[str]] = None):
    g_meta = config.pop("meta", {})
    routines = routines or g_meta.get("defaults", config.keys())
    for name in routines:
        with console.status(f"processing {name}"):
            meta = config[name].pop("meta", None)
            steps = config[name]["step"]
            for step in steps:
                i_type = step.pop("type")

                # Interpolate meta data into step values.
                if meta:
                    for key, val in step.items():
                        step[key] = val.format(**meta)

                step = registry[i_type](g_meta, **step)
                yield step
