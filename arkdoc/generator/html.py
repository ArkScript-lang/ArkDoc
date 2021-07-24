#!/usr/bin/env python3

import re
from datetime import datetime
import shutil
from typing import List
from pprint import pformat
from pathlib import Path

from . import specification as spec
from . import Generator
from .. import logger
from ..parser import Parser


def make_nav_link(name: str, path: str) -> str:
        return f"<a href=\"{path}\" class=\"btn btn-link\">{name}</a>"


def make_code_block(content: str) -> str:
    return f"""<pre>
<code class="rainbowjs" data-language="arkscript">
{content}
</code>
</pre>"""


def make_section(title: str, content: str) -> str:
    return f"""<section id="examples">
<h2>{title}</h2>

<div class="inner-section">
    {content}
</div>
</section>"""


def make_unordered_list(content: List[str]) -> str:
    out = "<ul>"
    for el in content:
        out += f"<li>{el}</li>"
    return out + "</ul>"


class HTMLGenerator(Generator):
    def __init__(self, parsers: List[Parser], output: str, ark_version: str):
        super().__init__(parsers, spec.HTML_TEMPLATE_FOLDER, "*.html")

        self.version = ark_version
        self.output_path = Path(output)
        self.output_path_ver = self.output_path / self.version

        self.fields = {
            name: re.findall(r"{\w+}", content, re.MULTILINE)
            for name, content in self.templates.items()
        }

        self.footer = f"Last generation at {datetime.now()}"

    def create_dir(self, name: str):
        (self.output_path / name).mkdir()

    def generate_index(self):
        if not self.output_path_ver.exists():
            if not (self.template_folder / "assets").exists():
                shutil.copytree(str(self.template_folder / "assets"), str(self.output_path / "assets"))
            self.output_path_ver.mkdir()
        else:
            shutil.rmtree(str(self.output_path_ver))
            return self.generate_index()

        sections = make_section(
            f"ArkScript {self.version} documentation",
            f"Welcome! This is the official documentation for ArkScript {self.version}" +
                make_unordered_list([file.path for file in self.list.files])
        )

        content = self.templates["index.html"]
        content = content.format(
            page_title=f"ArkScript {self.version} documentation",
            banner=self.templates["banner.html"],
            navigation_links="",
            sections=sections,
            footer=self.footer
        )

        (self.output_path_ver / "index.html").write_text(content)
        logger.info("Generated", self.output_path_ver / "index.html")

    def generate_one(self, path: str, functions: List[spec.Function]):
        local_fields = self.fields.copy()
        return None
