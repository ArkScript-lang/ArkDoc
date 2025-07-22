#!/usr/bin/env python3

import shutil
from datetime import datetime
from typing import List

from . import specification as spec, Formatter
from . import Generator
from .. import logger
from ..parser import Parser


class HTMLFormatter(Formatter):
    def nav_item(self, name: str, anchor: str) -> str:
        return f"""<li class="nav-item">
    <a href="#{anchor}">{name}</a>
</li>"""

    def a(self, name: str, path: str) -> str:
        return f'<a href="{path}">{name}</a>'

    def b(self, content: str) -> str:
        return f"<b>{content}</b>"

    def inline_code(self, content: str) -> str:
        return f"<code>{content}</code>"

    def code(self, content: str) -> str:
        return f"""<pre>
<code class="rainbowjs" data-language="arkscript">
{content}
</code>
</pre>"""

    def section(self, title: str, content: str, anchor: str = "") -> str:
        return f"""<section {f'id="{anchor}"' if anchor else ''}>
    <h2>{title}</h2>

    <div class="inner-section">
        {content}
    </div>
</section>"""

    def ul(self, content: List[str]) -> str:
        out = "<ul>"
        for el in content:
            out += f"<li>{el}</li>"
        return out + "</ul>"

    def div(self, *args: str) -> str:
        return "<div>" + "\n".join(args) + "</div>"

    def h1(self, name: str) -> str:
        return f"<h1>{name}</h1>"

    def h2(self, name: str) -> str:
        return f"<h2>{name}</h2>"

    def h3(self, name: str) -> str:
        return f"<h3>{name}</h3>"

    def h4(self, name: str) -> str:
        return f"<h4>{name}</h4>"

    def hr(self) -> str:
        return "<hr>"

    def new_line(self) -> str:
        return "<br>"


class HTMLGenerator(Generator):
    def __init__(self, parsers: List[Parser], output: str, ark_version: str, root: str):
        super().__init__(
            parsers, spec.HTML_TEMPLATE_FOLDER, HTMLFormatter(), "*.html", output, ark_version, root
        )

        self.footer = f"<i>Last generation at {datetime.now()}</i>"

    def generate_index(self):
        if not (self.output_path / "assets").exists():
            shutil.copytree(
                str(self.template_folder / "assets"), str(self.output_path / "assets")
            )

        sections = self.formatter.section(
            f"ArkScript {self.version} documentation",
            f"Welcome! This is the official documentation for ArkScript {self.version}"
            + self.formatter.ul(
                [
                    self.formatter.a(file.path, f"{self.root}/{self.version}/{file.path}.html")
                    for file in self.list.files
                ]
            ),
        )

        content = self.templates["index.html"]
        content = content.format(
            root=self.root,
            page_title=f"ArkScript {self.version} documentation",
            home_link=f"{self.root}/{self.version}",
            banner=self.templates["banner.html"].format(root=self.root),
            table_of_content="",
            navigation_links="",
            sections=sections,
            footer=self.footer,
        )

        (self.output_path_ver / "index.html").write_text(content)
        logger.info("Generated", self.output_path_ver / "index.html")

    def generate_one(self, path: str, functions: List[spec.Function]):
        sections = self.generate_sections(functions, with_hr=False)

        table_of_content = self.templates["table_of_content.html"]
        links = ""
        for func in functions:
            links += self.formatter.nav_item(func.name, self.formatter.anchorize(func.name))

        table_of_content = table_of_content.format(table_of_content_links=links)

        content = self.templates["index.html"]
        content = content.format(
            root=self.root,
            page_title=f"{path} - ArkScript {self.version} documentation",
            home_link=f"{self.root}/{self.version}",
            banner="",
            table_of_content=table_of_content,
            navigation_links="",
            sections=sections,
            footer=self.footer,
        )

        (self.output_path_ver / f"{path}.html").write_text(content)
        return None
