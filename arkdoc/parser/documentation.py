#!/usr/bin/env python3

from dataclasses import dataclass
from collections.abc import Iterable
from typing import List
from enum import Enum

from .tokenizer import Token


def deep_flatten(lst):
    return ([a for i in lst for a in
             deep_flatten(i)] if isinstance(lst, Iterable) else [lst])


class Source(Enum):
    ArkScript = 0
    Cpp = 1


@dataclass
class Documentation:
    source: Source
    comments: List[Token]
    target: List

    def _token_format(self, token: Token):
        return token.value

    def signature(self, on: List[Token] = None):
        def transform(L): return list(
            map(lambda t: t.value, deep_flatten(L)))
        top = self.target[:] if on is None else on

        while True:
            if isinstance(top, list) and \
                    len(top) and isinstance(top[0], list):
                top = top[0]
            else:
                break

        if on is None:
            return transform(top[:2]) + self.signature(on=top[2])
        else:
            return transform(top[1:2])

    @property
    def pretty_signature(self):
        kw, name, *args = self.signature()
        return f"({kw} {name} (fun ({' '.join(args)}) (...)))"

    @property
    def defined_at(self):
        return deep_flatten(self.target[:])[0].line

    def __str__(self):
        return f"Documentation({len(self.comments)} comments, {self.pretty_signature}, line={self.defined_at})"
