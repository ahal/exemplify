import os
import sys
from argparse import ArgumentParser
from pathlib import Path

from dittoed import synchronize, parse_config, generate_installables


def run(args=sys.argv[1:]):
    parser = ArgumentParser()
    parser.add_argument("routines", nargs="*", help="Routines to synchronize")
    parser.add_argument(
        "--list", default=False, action="store_true", help="List available routines"
    )

    args = parser.parse_args(args)

    config_path = Path(os.getcwd()) / "ditto.toml"
    config = parse_config(str(config_path))

    if args.list:
        routines = [key for key in config.keys() if key != "meta"]
        print("\n".join(sorted(routines)))
        return

    for installable in generate_installables(config, routines=args.routines):
        synchronize(installable)
