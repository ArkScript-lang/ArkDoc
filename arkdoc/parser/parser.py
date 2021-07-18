#!/usr/bin/env python3

import re
from typing import List
from dataclasses import dataclass
from collections.abc import Iterable

from .. import logger
from .tokenizer import tree_from_tokens, tokenize, Token


def deep_flatten(lst):
    return ([a for i in lst for a in
             deep_flatten(i)] if isinstance(lst, Iterable) else [lst])


@dataclass
class Documentation:
    comments: List[Token]
    target: List

    def _token_format(self, token: Token):
        return token.value

    def extract_signature(self, on: List[Token] = None):
        top = self.target[:] if on is None else on
        while True:
            if isinstance(top, list) and \
                    len(top) and isinstance(top[0], list):
                top = top[0]
            else:
                break

        transform = lambda L: list(map(lambda t: t.value, deep_flatten(L)))

        if on is None:
            return transform(top[:2]) + self.extract_signature(on=top[2])
        else:
            return transform(top[1:2])

    def __str__(self):
        return f"Documentation({len(self.comments)} comments, {self.extract_signature()})"


class Parser:
    def __init__(self, filename: str):
        self.filename = filename
        self.ast = None

    def visit(self, node: List, depth: int = 0):
        for n in node:
            if not isinstance(n, list):
                logger.debug(depth * " ", n)
            else:
                self.visit(n, depth + 1)

    def _is_doc_comment(self, token: Token) -> bool:
        return token.type == 'COMMENT' and re.match(
            r'^#+ *@\w+', token.value
        ) is not None

    def extract_doc(self, node: List):
        doc = None

        for n in node:
            if not isinstance(n, list):
                if self._is_doc_comment(n):
                    if doc is None:
                        doc = Documentation([], None)
                    doc.comments.append(n)
            elif doc is None:
                self.extract_doc(n)
            else:
                doc.target = n
                yield doc
                doc = None

                yield from self.extract_doc(n)

    def parse(self):
        with open(self.filename, 'r') as f:
            program = f.read()

        self.ast = tree_from_tokens(list(tokenize(program)))
        # self.visit(self.ast)

        for e in self.extract_doc(self.ast):
            logger.debug(e)
