#!/usr/bin/env python3

from . import specification

from .. import logger


class CodeToHTML:
    def __init__(self, list: specification.FileList):
        self.list = list
        self.template = (specification.TEMPLATE_FOLDER / "temp.html").read_text('utf-8')

    def generate(self):
        for file in self.list.files:
            logger.info(f"Generating {file.path} documentation...")
            logger.info(f"Found {len(file.functions)} functions")

            for func in file.functions:
                logger.debug(func)
