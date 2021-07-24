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


class HTMLGenerator(Generator):
    def __init__(self, parsers: List[Parser], output: str):
        super().__init__(parsers, spec.HTML_TEMPLATE_FOLDER, "*.html")
        self.output_path = Path(output)
        self.fields = {
            name: re.findall(r"{\w+}", content, re.MULTILINE)
            for name, content in self.templates.items()
        }

        self.footer = f"Last generation at {datetime.now()}"

    def make_nav_link(self, name: str, path: str) -> str:
        return f"<a href=\"{path}\" class=\"btn btn-link\">{name}</a>"

    def make_code_block(self, content: str) -> str:
        return f"""<pre>
<code class="rainbowjs" data-language="arkscript">
{content}
</code>
</pre>"""

    def make_section(self, title: str, content: str) -> str:
        return f"""<section id="examples">
    <h2>{title}</h2>

    <div class="inner-section">
        {content}
    </div>
</section>"""

    def create_dir(self, name: str):
        (self.output_path / name).mkdir()

    def generate_index(self):
        if not self.output_path.exists():
            shutil.copytree(str(self.template_folder / "assets"), str(self.output_path / "assets"))
        else:
            shutil.rmtree(str(self.output_path))
            if self.output_path.exists():
                self.output_path.rmdir()
            return self.generate_index()

        sections = self.make_section("Test", "test")

        content = self.templates["index.html"]
        content = content.format(
            page_title="ArkScript documentation",
            banner=self.templates["banner.html"],
            navigation_links="",
            sections=sections,
            footer=self.footer
        )

        (self.output_path / "index.html").write_text(content)

    def generate_one(self, path: str, functions: List[spec.Function]):
        local_fields = self.fields.copy()
        return None
