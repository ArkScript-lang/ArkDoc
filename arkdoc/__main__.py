#!/usr/bin/env python3

import os
import sys
import argparse

from arkdoc.generator.utils import extractor
from arkdoc.parser import Source
from . import logger
from .logger_utils import LogLevel
from .reader import parse_all_in
from .generator import HTMLGenerator


EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def check_folders(source_folder) -> bool:
    global logger

    for folder in source_folder:
        if not os.path.exists(folder):
            logger.error(f"Folder `{folder}` does not exists")
            return False
    return True


def parse_all(source_folder, dry_run) -> list:
    global logger

    parsers = []
    for folder in source_folder:
        parsers += parse_all_in(folder)
    for p in parsers:
        logger.info(f"Parsing {p.filename}...")
        p.parse()

        if dry_run:
            _ = list(p.extract_documentation())

    return parsers

def compute(args) -> bool:
    global logger

    if not check_folders(args.source_folder):
        return False
    if args.dry_run:
        logger.level = LogLevel.DEBUG

    parsers = parse_all(args.source_folder, args.dry_run)

    if not args.dry_run:
        if args.extract_func_names:
            functions = []
            for p in parsers:
                prefix = os.path.splitext(os.path.basename(p.filename))[0].lower()
                for doc in p.extract_documentation():
                    if doc.source == Source.ArkScript:
                        kw, name, *args = doc.signature()
                        if kw == "$":
                            # macro!
                            functions.append(name)
                        else:
                            functions.append(prefix + ":" + name)
                    elif doc.source == Source.Cpp:
                        data, _ = extractor({"name": ""}, doc)
                        functions.append(data["name"])
            print("\n".join(functions))
            # early exit if the flag is present
            return True

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
    cli.add_argument(
        "--extract-func-names",
        action="store_true",
        help="Extract only the function names, print them on separate lines and exit",
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
