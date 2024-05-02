import os
import sys
from argparse import ArgumentParser

from exemplify.main import exemplify


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
    exemplify(args.exemplar, routines=args.routines, verbose=args.verbose)
