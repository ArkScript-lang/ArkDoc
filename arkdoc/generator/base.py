#!/usr/bin/env python3

import shutil
import os
from typing import List
from pathlib import Path

from . import specification as spec, Formatter
from . import documentation_to_specification
from .. import logger
from ..parser import Parser


class Generator:
    def __init__(
            self,
            parsers: List[Parser],
            template_folder: Path,
            formatter: Formatter,
            pattern: str,
            output: str,
            ark_version: str,
            root: str,
    ):
        self.template_folder = template_folder
        self.formatter = formatter
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

        self.list.files = sorted(
            [f for f in self.list.files if len(f.functions)], key=lambda file: file.path
        )

    def generate_index(self):
        raise NotImplementedError

    def generate_sections(self, functions: List[spec.Function], with_hr: bool=False):
        sections = ""

        for func in functions:
            authors = (
                self.formatter.div(
                    self.formatter.b(self.formatter.plural("Author", len(func.desc.authors))),
                    ": ",
                    ", ".join(
                        [self.formatter.a(f"@{a.split('/')[-1]}", a) for a in func.desc.authors]
                    ),
                )
                if func.desc.authors
                else ""
            )
            parameters = (
                self.formatter.div(
                    self.formatter.h4(self.formatter.plural("Parameter", len(func.desc.params))),
                    self.formatter.ul(
                        [
                            f"{self.formatter.inline_code(p.name)}: {p.desc}"
                            for p in func.desc.params
                        ]
                    ),
                )
                if func.desc.params
                else ""
            )
            content = self.formatter.div(
                self.formatter.div(self.formatter.inline_code(func.signature)),
                self.formatter.div(func.desc.brief),
                self.formatter.new_line(),
                self.formatter.div(self.formatter.b("Note"), ": ", func.desc.details) if func.desc.details else "",
                self.formatter.new_line(),
                authors,
                self.formatter.new_line(),
                parameters,
            )
            if func.desc.code:
                content += self.formatter.div(self.formatter.h4("Example"), self.formatter.code(func.desc.code))
            sections += self.formatter.section(
                func.name,
                (self.formatter.hr() if with_hr else "") + content,
                anchor=self.formatter.anchorize(func.name)
            )

        return sections

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
