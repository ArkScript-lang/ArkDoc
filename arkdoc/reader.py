#!/usr/bin/env python3

import glob
from typing import List

from .parser import Parser


def explore(folder: str) -> List[str]:
    for ext in ["ark", "cpp"]:
        yield from glob.glob(f"{folder}/*.{ext}", recursive=True)


def parse_all_in(folder: str) -> List[Parser]:
    parsers = []
    for f in explore(folder):
        parsers.append(Parser(f))
    return parsers
