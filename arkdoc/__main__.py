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

    for folder in args.source_folder:
        if not os.path.exists(folder):
            logger.error(f"Folder `{folder}` does not exists")
            return False

    if args.dry_run:
        logger.level = LogLevel.DEBUG

    parsers = []
    for folder in args.source_folder:
        parsers += parse_all_in(folder)
    for p in parsers:
        logger.info(f"Parsing {p.filename}...")
        p.parse()

        if args.dry_run:
            _ = list(p.extract_documentation())

    if not args.dry_run:
        if args.html:
            gen = HTMLGenerator(parsers, args.html, args.ark_version, args.root_dir)
            gen()
        else:
            logger.error("Missing generator!")
            return False

    return True


def main() -> int:
    cli = argparse.ArgumentParser(description="ArkScript Documentation generator")
    cli.add_argument("ark_version", type=str, help="ArkScript version number, eg 3.1.0")
    cli.add_argument(
        "source_folder", type=str, help="Path to the ArkScript source folder", nargs="+"
    )
    cli.add_argument(
        "--dry-run",
        action="store_true",
        help="Run and log everything but don't generate any file",
    )
    cli.add_argument("--html", type=str, help="Output folder for the HTML docs")
    cli.add_argument(
        "--root-dir", type=str, default="", help="The root dir for the links"
    )

    args = cli.parse_args()

    if compute(args):
        return EXIT_SUCCESS
    else:
        return EXIT_FAILURE


if __name__ == "__main__":
    sys.exit(main())
