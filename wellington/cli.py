import os
import sys
from argparse import ArgumentParser
from pathlib import Path

import tomli

from wellington.installables.base import registry


here = os.path.abspath(os.path.dirname(__file__))


def install(item):
    if not item.enabled():
        return
    if item.exists():
        return
    print("####")
    print(item)
    print("####")
    item.install()


def update(item):
    if not item.enabled():
        return
    print("####")
    print(item)
    print("####")
    if item.exists():
        item.update()
    else:
        item.install()


def parse_config(path):
    with open(path) as fh:
        return tomli.load(fh)


def generate_installables(config, routines=None):
    routines = routines or config["meta"].get("defaults", config["routine"].keys())
    for name in routines:
        routine_obj = config["routine"][name]
        for step in routine_obj:
            i_type = step.pop("type")
            installable = registry[i_type](**step)
            yield installable


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

    config_path = Path(os.getcwd()) / "wellington.toml"
    config = parse_config(config_path)

    if getattr(args, "list", False):
        print("\n".join(config["routine"].keys()))
        return

    for installable in generate_installables(config, routines=args.routines):
        args.func(installable)
