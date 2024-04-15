import os
import sys
from argparse import ArgumentParser
from pathlib import Path

from dittoed import install, update, parse_config, generate_installables


def run(args=sys.argv[1:]):
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    install_parser = subparsers.add_parser("install")
    install_parser.add_argument("routines", nargs="*", help="Routines to install")
    install_parser.set_defaults(func=install)

    update_parser = subparsers.add_parser("update")
    update_parser.add_argument(
        "routines", nargs="*", default=None, help="Routines to update"
    )
    update_parser.set_defaults(func=update)

    list_parser = subparsers.add_parser("list")
    list_parser.set_defaults(**{"list": True})
    args = parser.parse_args(args)

    config_path = Path(os.getcwd()) / "ditto.toml"
    config = parse_config(str(config_path))

    if getattr(args, "list", False):
        routines = [key for key in config.keys() if key != "meta"]
        print("\n".join(sorted(routines)))
        return

    for installable in generate_installables(config, routines=args.routines):
        args.func(installable)
