import os

import tomli

from exemplify.steps.base import Step, registry
from exemplify.util.merge import merge


def synchronize(step: Step) -> int:
    if not step.enabled():
        return 0

    return step.sync()


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


def generate_steps(name: str, config: dict):
    routine = config[name]
    routine_meta = routine.get("meta")
    for step in routine["step"]:
        # Interpolate meta data into step values.
        if routine_meta:
            for key, val in step.items():
                step[key] = val.format(**routine_meta)

        stepcls = registry[step.pop("type")]
        step = stepcls(config.get("meta"), **step)
        yield step
