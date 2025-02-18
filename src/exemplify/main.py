import os
from pathlib import Path
from typing import Optional

import tomli
from rich.console import Console

console = Console()


def parse_config(path: str) -> dict:
    from exemplify.util.merge import merge

    root_path = os.path.dirname(path)

    with open(path, "rb") as fh:
        data = tomli.load(fh)

    data.setdefault("meta", {})
    for item in data["meta"].pop("include", []):
        path = os.path.join(root_path, f"{item}.toml")
        data = merge(parse_config(path), data)

    data["meta"]["root"] = root_path
    return data


def discover_config(exemplar: Path):
    if exemplar.suffix == ".toml":
        return exemplar

    path = Path(exemplar) / "exemplify.toml"
    if path.is_file():
        return path

    raise Exception(f"Config not found for {exemplar}!")


def generate_steps(name: str, config: dict):
    from exemplify.steps.base import registry

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


def exemplify(
    exemplar_path: str, routines: Optional[list[str]] = None, verbose: bool = False
) -> int:
    from exemplify.util import process

    process.VERBOSE = verbose

    exemplar = Path(exemplar_path).resolve()
    config_path = discover_config(exemplar)
    config = parse_config(str(config_path))

    routines = routines or config["meta"].get("defaults")
    if not routines:
        routines = [k for k in config.keys() if k != "meta"]

    ret = 0
    for name in routines:
        console.rule(f"Routine [blue]{name.upper()}", align="left")

        for step in generate_steps(name, config):
            print(f"{step} ", end=".. ", flush=True)

            result = step.sync()
            ret |= result

            if result == 0:
                msg = ":white_heavy_check_mark:"
            else:
                msg = ":x:"

            if verbose or result != 0:
                msg = f"{msg} return code: {result}"
            else:
                msg = f"{msg}"

            console.print(msg)

    return ret
