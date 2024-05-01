import inspect
import os
import sys
from argparse import ArgumentParser
from itertools import chain
from pathlib import Path

from rich.console import Group
from rich.live import Live
from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
)

from exemplify.console import RoutineProgress, console
from exemplify import generate_steps, parse_config


def discover_config(exemplar: Path):
    if exemplar.suffix == ".toml":
        return exemplar

    path = Path(exemplar) / "exemplify.toml"
    if path.is_file():
        return path

    raise Exception(f"Config not found for {exemplar}!")


def run(args=sys.argv[1:]):
    parser = ArgumentParser()
    parser.add_argument(
        "exemplar", default=os.getcwd(), help="Exemplar to synchronize with"
    )
    parser.add_argument(
        "--routine",
        dest="routines",
        default=None,
        action="append",
        help="Limit to specified routines",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    args = parser.parse_args(args)

    exemplar = Path(args.exemplar).resolve()
    config_path = discover_config(exemplar)
    config = parse_config(str(config_path))

    routines = args.routines or config["meta"].get("defaults")
    if not routines:
        routines = [k for k in config.keys() if k != "meta"]

    routine_progress = []
    num_steps = 0
    for name in routines:
        routine_progress.append(RoutineProgress(name, display_output=args.verbose))

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
            progress.update(
                description=f"[bold]Routine [blue]{progress.routine}[/blue] processing.."
            )

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
                                progress.step.append_output(output.strip())
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
            if progress.returncode == 0:
                progress.update(
                    description=f"[bold green]Routine [blue]{progress.routine}[/blue] succeeded!",
                )
            else:
                progress.update(
                    description=f"[bold red]Routine [blue]{progress.routine}[/blue] failed!",
                )

        overall_progress.update(overall_task_id, visible=False)
