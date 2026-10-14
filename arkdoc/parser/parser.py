#!/usr/bin/env python3

import re
from typing import List

from . import Documentation, Source
from .tokenizer import generic_tokenizer, CPP_COMMENT_REGEX, TXT_COMMENT_REGEX, tree_from_tokens, tokenize, Token
from .. import logger


class Parser:
    def __init__(self, filename: str):
        self.filename = filename
        self.ast = None
        self.in_code = False
        self.in_details = False

    def _is_doc_comment(self, token: Token) -> bool:
        if token.type == "COMMENT":
            if "=begin" in token.value:
                self.in_code = True
                return True
            if "=details-begin" in token.value:
                self.in_details = True
                return True
            if "=end" not in token.value and self.in_code:
                return True
            if "=details-end" not in token.value and self.in_details:
                return True
            if "=end" in token.value:
                self.in_code = False
                return True
            if "=details-end" in token.value:
                self.in_details = False
                return True

            return re.match(r"^#+ *@\w+", token.value) is not None
        return False

    def _doc_extractor(self, node: List):
        comments = None

        for n in node:
            if not isinstance(n, list):
                if self._is_doc_comment(n):
                    comments = [n] if comments is None else comments + [n]
                if n.type == "EMPTY_LINE" and comments is not None:
                    yield Documentation(Source.ArkScript, comments, None)
                    comments = None
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
        elif self.filename.endswith(".txt"):
            for node in self.ast:
                yield Documentation(Source.Txt, node, None)
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
            self.ast = list(generic_tokenizer(CPP_COMMENT_REGEX, program))
            logger.debug(self.ast)
        elif self.filename.endswith(".txt"):
            self.ast = list(generic_tokenizer(TXT_COMMENT_REGEX, program))
            logger.debug(self.ast)
        else:
            logger.error(f"Could not parse {self.filename}")
