#!/usr/bin/env python3

from typing import List
from dataclasses import dataclass
from pathlib import Path


HTML_TEMPLATE_FOLDER = Path("templates")

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


@dataclass
class File:
    path: str
    functions: List[Function]


@dataclass
class FileList:
    files: List[File]
