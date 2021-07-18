#!/usr/bin/env python3

from typing import List
from pprint import pformat

from . import specification as spec
from . import Generator
from .. import logger
from ..parser import Parser


class HTMLGenerator(Generator):
    def __init__(self, parsers: List[Parser]):
        super().__init__(parsers, spec.HTML_TEMPLATE_FOLDER / "temp.html")

    def _generate(self, path: str, functions: List[spec.Function]):
        # TODO
        logger.info(path, pformat(functions, indent=4))
        return None
