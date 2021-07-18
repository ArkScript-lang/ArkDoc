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


def main() -> int:
    cli = argparse.ArgumentParser(
        description='ArkScript Documentation generator'
    )
    cli.add_argument(
        'source_folder',
        type=str,
        help='Path to the ArkScript source folder'
    )
    cli.add_argument(
        '--dry-run',
        help='Run and log everything but don\'t generate any file'
    )

    args = cli.parse_args()

    if not os.path.exists(args.source_folder):
        logger.error(f"Folder `${args.source_folder}` does not exists")
        return EXIT_FAILURE

    if args.dry_run:
        logger.level = LogLevel.DEBUG

    parsers = parse_all_in(args.source_folder)
    for p in parsers:
        logger.info(f"Parsing {p.filename}...")
        p.parse()

        if args.dry_run:
            list(p.extract_documentation())

    if not args.dry_run:
        pass

    return EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
