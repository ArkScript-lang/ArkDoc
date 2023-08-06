#!/usr/bin/env python3

import re
from typing import List

from . import Documentation, Source
from .tokenizer import cpp_tokenize, tree_from_tokens, tokenize, Token
from .. import logger


class Parser:
    def __init__(self, filename: str):
        self.filename = filename
        self.ast = None
        self.in_code = False

    def _is_doc_comment(self, token: Token) -> bool:
        if token.type == "COMMENT":
            if "=begin" in token.value:
                self.in_code = True
                return True
            if "=end" not in token.value and self.in_code:
                return True
            if "=end" in token.value:
                self.in_code = False
                return True

            return re.match(r"^#+ *@\w+", token.value) is not None
        return False

    def _doc_extractor(self, node: List):
        comments = None

        for n in node:
            if not isinstance(n, list):
                if self._is_doc_comment(n):
                    comments = [n] if comments is None else comments + [n]
            else:
                if comments is None:
                    yield from self._doc_extractor(n)
                elif comments is not None:
                    yield Documentation(Source.ArkScript, comments, n)
                    comments = None
                    yield from self._doc_extractor(n)

    def extract_documentation(self):
        if self.filename.endswith(".ark"):
            for doc in self._doc_extractor(self.ast):
                logger.debug(doc)
                yield doc
        elif self.filename.endswith(".cpp"):
            for node in self.ast:
                yield Documentation(Source.Cpp, node, None)
        else:
            raise NotImplementedError

    def parse(self):
        with open(self.filename, "r") as f:
            program = f.read()

        if self.filename.endswith(".ark"):
            self.ast = []
            tokens = list(tokenize(program))

            while tokens:
                self.ast += tree_from_tokens(tokens)
        elif self.filename.endswith(".cpp"):
            self.ast = list(cpp_tokenize(program))
            logger.debug(self.ast)
        else:
            logger.error(f"Could not parse {self.filename}")
