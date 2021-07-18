#!/usr/bin/env python3

import os
from typing import List
from pathlib import Path

from . import specification as spec
from . import documentation_to_specification
from .. import logger
from ..parser import Parser


class Generator:
    def __init__(self, parsers: List[Parser], template: Path):
        self.template = template.read_text('utf-8')
        self.list = spec.FileList([])

        registered = {}

        for p in parsers:
            functions = []
            for doc in p.extract_documentation():
                functions.append(documentation_to_specification(doc))

            base = os.path.splitext(os.path.basename(p.filename))[0]
            if base in registered:
                registered[base].functions += functions
            else:
                file = spec.File(base, functions)
                registered[base] = file

            self.list.files.append(file)

    def _generate(self, path: str, functions: List[spec.Function]):
        raise NotImplementedError

    def __call__(self):
        for file in self.list.files:
            logger.info(f"Generating {file.path} documentation...")
            logger.info(f"\tFound {len(file.functions)} functions")

            self._generate(file.path, file.functions)
