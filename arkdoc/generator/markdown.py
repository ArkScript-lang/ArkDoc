#!/usr/bin/env python3

from datetime import datetime
from typing import List

from . import specification as spec, Formatter
from . import Generator
from .. import logger
from ..parser import Parser


class MarkdownFormatter(Formatter):
    def a(self, name: str, path: str) -> str:
        return f'[{name}]({path})'

    def b(self, content: str) -> str:
        return f"**{content}**"

    def inline_code(self, content: str) -> str:
        return f"`{content}`"

    def code(self, content: str) -> str:
        return f"""{{{{< highlight_arkscript >}}}}
{content}
{{{{< /highlight_arkscript >}}}}"""

    def section(self, title: str, content: str, anchor: str = "") -> str:
        return f"## {title}\n\n{content}\n"

    def ul(self, content: List[str]) -> str:
        out = ""
        for el in content:
            out += f"- {el}\n"
        return out

    def div(self, *args: str) -> str:
        return "".join(args) + "\n"

    def h1(self, name: str) -> str:
        return f"# {name}\n"

    def h2(self, name: str) -> str:
        return f"## {name}\n"

    def h3(self, name: str) -> str:
        return f"### {name}\n"

    def h4(self, name: str) -> str:
        return f"#### {name}\n"

    def hr(self) -> str:
        return "---\n"

    def new_line(self) -> str:
        return "\n"


class MDGenerator(Generator):
    def __init__(self, parsers: List[Parser], output: str, ark_version: str, root: str):
        super().__init__(parsers, spec.MD_TEMPLATE_FOLDER, MarkdownFormatter(), "*.md", output, ark_version, root)

        self.generated_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.decl_file = self.output_path_ver / "_decl.txt"

    def generate_index(self):
        sections = self.formatter.section(
            f"ArkScript {self.version} documentation",
            "",
        )

        content = self.templates["_index.md"]
        content = content.format(
            title="Standard library",
            date=self.generated_at,
            content=sections,
        )

        (self.output_path_ver / "_index.md").write_text(content)
        logger.info("Generated", self.output_path_ver / "_index.md")

        self.decl_file.touch()
        logger.info("Created", self.output_path_ver / "_decl.txt")

    def generate_one(self, path: str, functions: List[spec.Function]):
        sections = self.generate_sections(functions, with_hr=True)

        template = self.templates["page.md"]
        template = template.format(
            title=path,
            slug=self.formatter.anchorize(path),
            date=self.generated_at,
            content=sections,
        )

        (self.output_path_ver / f"{path}.md").write_text(template)

        for func in functions:
            with self.decl_file.open("a") as file:
                file.write(f"{func.signature}\n")
        return None
