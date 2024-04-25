import os
import sys
from argparse import ArgumentParser
from pathlib import Path

from exemplify.console import console
from exemplify import generate_steps, parse_config, synchronize


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

    args = parser.parse_args(args)

    exemplar = Path(args.exemplar).resolve()
    config_path = discover_config(exemplar)
    config = parse_config(str(config_path))

    routines = args.routines or config["meta"].get("defaults")
    if not routines:
        routines = [k for k in config.keys() if k != "meta"]

    for routine in routines:
        for step in generate_steps(routine, config):
            with console.status(f"Processing routine {routine}: STEP {step}"):
                with console.capture() as capture:
                    ret = synchronize(step)

                if ret == 0:
                    console.print(f":white_heavy_check_mark: {step}")
                else:
                    print(capture.get())
