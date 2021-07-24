#!/usr/bin/env python3

import re
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
        self.output = Path(output)
        self.fields = {
            name: re.findall(r"{\w+}", content, re.MULTILINE)
            for name, content in self.templates.items()
        }

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

    def _generate(self, path: str, functions: List[spec.Function]):
        logger.info("---- ", path)
        logger.info(pformat(functions, indent=4))
        return None
