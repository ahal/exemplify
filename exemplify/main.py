import inspect
import os
from itertools import chain
from pathlib import Path
from typing import Optional

import tomli
from rich.console import Group
from rich.live import Live
from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
)

from exemplify.console import RoutineProgress, console
from exemplify.steps.base import registry
from exemplify.util.merge import merge


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


def discover_config(exemplar: Path):
    if exemplar.suffix == ".toml":
        return exemplar

    path = Path(exemplar) / "exemplify.toml"
    if path.is_file():
        return path

    raise Exception(f"Config not found for {exemplar}!")


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


def exemplify(
    exemplar_path: str, routines: Optional[list[str]] = None, verbose: bool = False
) -> int:
    exemplar = Path(exemplar_path).resolve()
    config_path = discover_config(exemplar)
    config = parse_config(str(config_path))

    routines = routines or config["meta"].get("defaults")
    if not routines:
        routines = [k for k in config.keys() if k != "meta"]

    routine_progress = []
    num_steps = 0
    for name in routines:
        routine_progress.append(RoutineProgress(name, display_output=verbose))

        for step in generate_steps(name, config):
            num_steps += 1
            routine_progress[-1].step.add_step(step)

    overall_progress = Progress(
        TextColumn("Exemplify"),
        BarColumn(),
        TextColumn("{task.description}"),
    )
    overall_task_id = overall_progress.add_task("", total=num_steps)

    progress_group = Group(
        *chain.from_iterable((rp, rp.step) for rp in routine_progress),
        overall_progress,
    )

    with Live(
        progress_group,
        refresh_per_second=10,
        redirect_stdout=False,
        redirect_stderr=False,
    ):
        for idx, progress in enumerate(routine_progress):
            top_description = (
                f"[bold #AAAAAA]({idx} / {len(routine_progress)} routines complete)"
            )
            overall_progress.update(overall_task_id, description=top_description)

            progress.start_routine()

            while True:
                try:
                    step = next(progress.step)
                except StopIteration:
                    break

                with console.capture() as capture:
                    if not step.enabled():
                        ret = 0
                    elif inspect.isgeneratorfunction(step.sync):
                        sync = step.sync()
                        try:
                            while True:
                                output = next(sync)
                                progress.step.append_output(output)
                        except StopIteration as e:
                            ret = e.value
                    else:
                        ret = step.sync()

                captured_output = capture.get()
                if captured_output:
                    out = f"Captured output:\n{captured_output}"
                    progress.step.append_output(out)

                progress.step.set_status(ret)

                overall_progress.update(overall_task_id, advance=1)

            progress.stop_routine()

        overall_progress.update(overall_task_id, visible=False)
