#!/usr/bin/env python3

import os
import sys
import argparse

from . import logger
from .logger_utils import LogLevel
from .reader import parse_all_in
from .generator import HTMLGenerator


EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def compute(args) -> bool:
    global logger

    if not os.path.exists(args.source_folder):
        logger.error(f"Folder `${args.source_folder}` does not exists")
        return False

    if args.dry_run:
        logger.level = LogLevel.DEBUG

    parsers = parse_all_in(args.source_folder)
    if args.builtins:
        parsers += parse_all_in(args.builtins)
    for p in parsers:
        logger.info(f"Parsing {p.filename}...")
        p.parse()

        if args.dry_run:
            _ = list(p.extract_documentation())

    if not args.dry_run:
        if args.html:
            # TODO put a flag or find the version
            gen = HTMLGenerator(parsers, args.html, "3.1.0")
            gen()
        else:
            logger.error("Missing generator!")
            return False

    return True


def main() -> int:
    cli = argparse.ArgumentParser(description="ArkScript Documentation generator")
    cli.add_argument(
        "source_folder", type=str, help="Path to the ArkScript source folder"
    )
    cli.add_argument(
        "--builtins", type=str, help="Path to the builtins folder", default=None
    )
    cli.add_argument(
        "--dry-run",
        action="store_true",
        help="Run and log everything but don't generate any file",
    )
    cli.add_argument("--html", type=str, help="Output folder for the HTML docs")

    args = cli.parse_args()

    if compute(args):
        return EXIT_SUCCESS
    else:
        return EXIT_FAILURE


if __name__ == "__main__":
    sys.exit(main())
