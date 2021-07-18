#!/usr/bin/env python3

import os
import sys
import argparse

from . import logger
from .reader import parse_all_in


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

    args = cli.parse_args()

    if not os.path.exists(args.source_folder):
        logger.error(f"Folder `${args.source_folder}` does not exists")
        return EXIT_FAILURE

    parsers = parse_all_in(args.source_folder)
    for p in parsers:
        logger.info(f"Parsing {p.filename}...")
        p.parse()

    return EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
