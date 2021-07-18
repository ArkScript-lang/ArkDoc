#!/usr/bin/env python3

import re
from typing import List

from . import Documentation
from .tokenizer import tree_from_tokens, tokenize, Token
from .. import logger


class Parser:
    def __init__(self, filename: str):
        self.filename = filename
        self.ast = None

    def _is_doc_comment(self, token: Token) -> bool:
        return token.type == 'COMMENT' and re.match(
            r'^#+ *@\w+', token.value
        ) is not None

    def _doc_extractor(self, node: List):
        comments = None

        for n in node:
            if not isinstance(n, list):
                if self._is_doc_comment(n):
                    comments = [
                        n
                    ] if comments is None else comments + [n]
            else:
                if comments is None:
                    yield from self._doc_extractor(n)
                elif comments is not None:
                    yield Documentation(comments, n)
                    comments = None
                    yield from self._doc_extractor(n)

    def extract_documentation(self):
        for doc in self._doc_extractor(self.ast):
            logger.debug(doc)
            yield doc

    def parse(self):
        with open(self.filename, 'r') as f:
            program = f.read()

        self.ast = []
        tokens = list(tokenize(program))

        while tokens:
            self.ast += tree_from_tokens(tokens)
