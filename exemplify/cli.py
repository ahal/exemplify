import os
import sys
from argparse import ArgumentParser
from pathlib import Path

from exemplify import synchronize, parse_config, generate_steps


def run(args=sys.argv[1:]):
    parser = ArgumentParser()
    parser.add_argument("routines", nargs="*", help="Routines to synchronize")
    parser.add_argument(
        "--list", default=False, action="store_true", help="List available routines"
    )

    args = parser.parse_args(args)

    config_path = Path(os.getcwd()) / "exemplify.toml"
    config = parse_config(str(config_path))

    if args.list:
        routines = [key for key in config.keys() if key != "meta"]
        print("\n".join(sorted(routines)))
        return

    for step in generate_steps(config, routines=args.routines):
        synchronize(step)
