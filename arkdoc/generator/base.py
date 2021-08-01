#!/usr/bin/env python3

import shutil
import os
from typing import List
from pathlib import Path

from . import specification as spec
from . import documentation_to_specification
from .. import logger
from ..parser import Parser


class Generator:
    def __init__(
        self,
        parsers: List[Parser],
        template_folder: Path,
        pattern: str,
        output: str,
        ark_version: str,
        root: str,
    ):
        self.template_folder = template_folder
        self.templates = {
            file.name: file.read_text("utf-8") for file in template_folder.glob(pattern)
        }
        self.output_path = Path(output)
        self.version = ark_version
        self.output_path_ver = self.output_path / self.version
        self.root = root if root and root[-1] != "/" else root[:-1]
        self.list = spec.FileList([])
        self._create_files_list(parsers)

    def _create_files_list(self, parsers: List[Parser]):
        registered = {}

        for p in parsers:
            functions = []
            for doc in p.extract_documentation():
                functions.append(documentation_to_specification(doc))

            base = os.path.splitext(os.path.basename(p.filename))[0]
            if base in registered:
                registered[base].functions += functions
            else:
                registered[base] = spec.File(base, functions)
                self.list.files.append(registered[base])

        self.list.files = [f for f in self.list.files if len(f.functions)]

    def generate_index(self):
        raise NotImplementedError

    def generate_one(self, path: str, functions: List[spec.Function]):
        raise NotImplementedError

    def __call__(self):
        if not self.output_path_ver.exists():
            self.output_path_ver.mkdir(parents=True)
        else:
            shutil.rmtree(str(self.output_path_ver))
            return self.__call__()

        self.generate_index()

        for file in self.list.files:
            logger.info(
                f"Generating {file.path} documentation... found {len(file.functions)} functions"
            )

            self.generate_one(file.path, file.functions)
