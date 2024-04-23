import os
import sys
from argparse import ArgumentParser
from pathlib import Path

from exemplify import generate_steps, parse_config, synchronize


def discover_config(exemplar: Path):
    if exemplar.suffix == "toml":
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

    for step in generate_steps(config, routines=args.routines):
        synchronize(step)
