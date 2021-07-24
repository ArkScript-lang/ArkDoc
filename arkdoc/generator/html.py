#!/usr/bin/env python3

import shutil
from datetime import datetime
from typing import List
from pprint import pformat
from pathlib import Path

from . import specification as spec
from . import Generator
from .. import logger
from ..parser import Parser


class html:
    @staticmethod
    def plural(name: str, qu: int) -> str:
        return f"{name}{'s' if qu > 1 else ''}"

    @staticmethod
    def nav_link(name: str, path: str) -> str:
        return f"<a href=\"{path}\" class=\"btn btn-link\">{name}</a>"

    @staticmethod
    def anchorize(name: str) -> str:
        return name.lower().replace(" ", "-")

    @staticmethod
    def nav_item(name: str, anchor: str) -> str:
        return f"""<li class="nav-item">
    <a href="#{anchor}">{name}</a>
</li>"""

    @staticmethod
    def a(name: str, path: str) -> str:
        return f"<a href=\"{path}\">{name}</a>"

    @staticmethod
    def b(content: str) -> str:
        return f"<b>{content}</b>"

    @staticmethod
    def inline_code(content: str) -> str:
        return f"<code>{content}</code>"

    @staticmethod
    def code(content: str) -> str:
        return f"""<pre>
<code class="rainbowjs" data-language="arkscript">
{content}
</code>
</pre>"""

    @staticmethod
    def section(title: str, content: str, anchor: str="") -> str:
        return f"""<section {f'id="{anchor}"' if anchor else ''}>
    <h2>{title}</h2>

    <div class="inner-section">
        {content}
    </div>
</section>"""

    @staticmethod
    def ul(content: List[str]) -> str:
        out = "<ul>"
        for el in content:
            out += f"<li>{el}</li>"
        return out + "</ul>"

    @staticmethod
    def div(*args: List[str]) -> str:
        return "<div>" + "\n".join(args) + "</div>"

    @staticmethod
    def h1(name: str) -> str:
        return f"<h1>{name}</h1>"

    @staticmethod
    def h2(name: str) -> str:
        return f"<h2>{name}</h2>"

    @staticmethod
    def h3(name: str) -> str:
        return f"<h3>{name}</h3>"

    @staticmethod
    def h4(name: str) -> str:
        return f"<h4>{name}</h4>"


class HTMLGenerator(Generator):
    def __init__(self, parsers: List[Parser], output: str, ark_version: str):
        super().__init__(parsers, spec.HTML_TEMPLATE_FOLDER, "*.html", output, ark_version)

        self.footer = f"<i>Last generation at {datetime.now()}</i>"

    def create_dir(self, name: str):
        (self.output_path / name).mkdir()

    def generate_index(self):
        if not (self.output_path / "assets").exists():
            shutil.copytree(str(self.template_folder / "assets"), str(self.output_path / "assets"))

        sections = html.section(
            f"ArkScript {self.version} documentation",
            f"Welcome! This is the official documentation for ArkScript {self.version}" +
                html.ul([html.a(file.path, f"/{self.version}/{file.path}.html") for file in self.list.files])
        )

        content = self.templates["index.html"]
        content = content.format(
            page_title=f"ArkScript {self.version} documentation",
            home_link=f"/{self.version}",
            has_banner="has-banner",
            banner=self.templates["banner.html"],
            table_of_content="",
            navigation_links="",
            sections=sections,
            footer=self.footer
        )

        (self.output_path_ver / "index.html").write_text(content)
        logger.info("Generated", self.output_path_ver / "index.html")

    def generate_one(self, path: str, functions: List[spec.Function]):
        sections = ""
        table_of_content = self.templates["table_of_content.html"]
        links = ""

        for func in functions:
            links += html.nav_item(func.name, html.anchorize(func.name))
            content = html.div(
                html.inline_code(func.signature), "<br>",
                html.div(func.desc.brief),
                html.div(
                    html.b("Note"), ": ",
                    func.desc.details
                ),
                html.div(
                    html.h4(html.plural("Parameter", len(func.desc.params))),
                    html.ul([
                        f"{html.inline_code(p.name)}: {p.desc}" for p in func.desc.params
                    ])
                ),
                html.div(
                    html.h4(html.plural("Author", len(func.desc.authors))),
                    ", ".join([
                        html.a(f"@{a.split('/')[-1]}", a) for a in func.desc.authors
                    ])
                )
            )
            if func.desc.code:
                content += html.div(
                    html.h4("Example"),
                    html.code(func.desc.code)
                )
            sections += html.section(func.name, content, anchor=html.anchorize(func.name))

        table_of_content = table_of_content.format(table_of_content_links=links)

        content = self.templates["index.html"]
        content = content.format(
            page_title=f"{path} - ArkScript {self.version} documentation",
            home_link=f"/{self.version}",
            has_banner="",
            banner="",
            table_of_content=table_of_content,
            navigation_links="",
            sections=sections,
            footer=self.footer
        )

        (self.output_path_ver / f"{path}.html").write_text(content)
        return None
