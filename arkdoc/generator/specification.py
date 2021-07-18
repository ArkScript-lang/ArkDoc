#!/usr/bin/env python3

from typing import List
from dataclasses import dataclass


@dataclass
class Param:
    name: str
    desc: str


@dataclass
class Description:
    brief: str
    details: str
    params: List[Param]
    code: str
    authors: List[str]


@dataclass
class Function:
    name: str
    desc: Description


class File:
    def __init__(self, path: str):
        assert(
            path.endswith('.ark'),
            f"{path} isn't an ArkScript source file"
        )
        self.path = path


@dataclass
class FileList:
    files: List[File]
