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

    def _signature(self, on: List[Token] = None):
        transform = lambda L: list(map(lambda t: t.value, deep_flatten(L)))
        top = self.target[:] if on is None else on

        while True:
            if isinstance(top, list) and \
                    len(top) and isinstance(top[0], list):
                top = top[0]
            else:
                break

        if on is None:
            return transform(top[:2]) + self._signature(on=top[2])
        else:
            return transform(top[1:2])

    @property
    def function_signature(self):
        kw, name, *args = self._signature()
        return f"({kw} {name} (fun ({' '.join(args)}) (...)))"

    @property
    def defined_at(self):
        return deep_flatten(self.target[:])[0].line

    def __str__(self):
        return f"Documentation({len(self.comments)} comments, {self.function_signature}, line={self.defined_at})"


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
                    yield Documentation(comments, n)
                    comments = None
                    yield from self._doc_extractor(n)

    def extract_documentation(self):
        yield from self._doc_extractor(self.ast)

    def parse(self):
        with open(self.filename, 'r') as f:
            program = f.read()

        self.ast = []
        tokens = list(tokenize(program))

        while tokens:
            self.ast += tree_from_tokens(tokens)
        # self.visit(self.ast)

        for e in self.extract_documentation():
            logger.debug(e)
