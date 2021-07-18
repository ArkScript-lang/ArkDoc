#!/usr/bin/env python3

import os
import sys
import argparse

from . import logger


EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description='ArkScript Documentation generator'
    )
    parser.add_argument(
        'source_folder',
        type=str,
        help='Path to the ArkScript source folder'
    )

    args = parser.parse_args()

    if not os.path.exists(args.source_folder):
        logger.error(f"Folder `${args.source_folder}` does not exists")
        return EXIT_FAILURE

    return EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
