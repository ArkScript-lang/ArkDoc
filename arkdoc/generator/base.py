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
            for i, doc in enumerate(p.extract_documentation()):
                try:
                    functions.append(documentation_to_specification(doc))
                except Exception as e:
                    logger.error(f"Error while parsing documentation block no {i + 1} inside {p.filename}")
                    print()
                    for comment in doc.comments:
                        logger.error(comment.value)
                    print()
                    raise e

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

    def __format_authors(self, func: spec.Function):
        return (
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

    def __format_params(self, func: spec.Function):
        return (
            self.formatter.div(
                self.formatter.h4(self.formatter.plural("Parameter", len(func.desc.params))),
                self.formatter.ul(
                    [
                        f"{self.formatter.inline_code(p.name)}: {p.desc}" if p.desc else self.formatter.inline_code(
                            p.name)
                        for p in func.desc.params
                    ]
                ),
            )
            if func.desc.params
            else ""
        )

    def __format_deprecation(self, func: spec.Function):
        return (
            self.formatter.div(
                self.formatter.b("Deprecated"),
                ": ",
                func.desc.deprecation_notice,
                self.formatter.new_line()
            )
            if func.desc.deprecation_notice
            else ""
        )

    def __format_changes(self, func: spec.Function):
        return (
            self.formatter.div(
                self.formatter.b("Changes"),
                ":",
                self.formatter.new_line(),
                self.formatter.ul(
                    [
                        f"{self.formatter.b(c.version)}: {c.desc}"
                        for c in sorted(func.desc.changelist, key=lambda change: change.version, reverse=True)
                    ]
                ),
                self.formatter.new_line()
            )
            if func.desc.changelist
            else ""
        )

    def __format_requirement(self, func: spec.Function):
        return (
            self.formatter.div(
                self.formatter.note(
                    f"ArkScript {func.desc.require.version}",
                    func.desc.require.desc
                ),
                self.formatter.new_line()
            )
            if func.desc.require
            else ""
        )

    def __format_doc(self, func: spec.Function):
        authors = self.__format_authors(func)
        parameters = self.__format_params(func)
        maybe_deprecated_notice = self.__format_deprecation(func)
        maybe_changelists = self.__format_changes(func)
        maybe_requirement = self.__format_requirement(func)

        content = self.formatter.div(
            self.formatter.div(self.formatter.inline_code(func.signature)),
            self.formatter.div(func.desc.brief),
            self.formatter.new_line(),
            maybe_requirement,
            maybe_deprecated_notice,
            maybe_changelists,
            self.formatter.div(
                self.formatter.b("Note"), ": ",
                self.formatter.new_line().join(func.desc.details)) if func.desc.details else "",
            self.formatter.new_line(),
            authors,
            self.formatter.new_line(),
            parameters,
        )
        if func.desc.code:
            content += self.formatter.div(self.formatter.h4("Example"), self.formatter.code(func.desc.code))

        return content

    def generate_sections(self, functions: List[spec.Function], with_hr: bool = False):
        sections = ""

        for func in functions:
            if func.desc.section:
                if sections:
                    sections += self.formatter.hr()
                sections += self.formatter.div(
                    self.formatter.div(func.desc.brief),
                    self.formatter.new_line(),
                    self.formatter.div(
                        self.formatter.new_line().join(func.desc.details) if func.desc.details else ""),
                    self.formatter.new_line(),
                    self.__format_deprecation(func),
                    self.__format_requirement(func),
                    self.__format_changes(func)
                )
            else:
                sections += self.formatter.section(
                    func.name,
                    (self.formatter.hr() if with_hr else "") + self.__format_doc(func),
                    anchor=self.formatter.anchorize(func.name)
                )

        return sections

    def generate_one(self, file: spec.File):
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
            self.generate_one(file)
        return None
