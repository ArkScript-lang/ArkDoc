#!/usr/bin/env python3

from typing import List

from . import specification as spec
from . import Generator
from .. import logger
from ..parser import Parser


class HTMLGenerator(Generator):
    def __init__(self, parser: Parser):
        super().__init__(parser, spec.HTML_TEMPLATE_FOLDER / "temp.html")

    def _generate(self, path: str, functions: List[spec.Function]):
        logger.debug(path, functions)
        return None
