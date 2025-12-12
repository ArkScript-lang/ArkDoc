#!/usr/bin/env python3

from dataclasses import dataclass
from collections.abc import Iterable
from typing import List
from enum import Enum

from .tokenizer import Token
from .. import logger


def deep_flatten(lst):
    return (
        [a for i in lst for a in deep_flatten(i)]
        if isinstance(lst, Iterable)
        else [lst]
    )


class Source(Enum):
    ArkScript = 0
    Cpp = 1


@dataclass
class Documentation:
    source: Source
    comments: List[Token]
    target: List

    macro_keywords = ("$", "macro")

    def signature(self):
        def transform(L):
            out = []
            for t in L:
                if isinstance(t, list) and len(t) == 1 and isinstance(t[0], list) and len(t[0]) == 2:
                    out.append(f"({t[0][0].value} {t[0][1].value})")
                elif not isinstance(t, list):
                    out.append(t.value)
                else:
                    raise NotImplementedError(f"token not parsed correctly in arglist: {t}")
            return out

        top = self.target[:]

        while True:
            if isinstance(top, list) and len(top) and isinstance(top[0], list):
                top = top[0]
            else:
                break

        kw, name = top[:2]

        if isinstance(top[2], list) and len(top[2][0]) >= 2:
            if kw.value not in self.macro_keywords:
                args = transform(top[2][0][1][0])
            else:
                args = transform(top[2][0])
            return [kw.value, name.value, args]
        else:
            return [kw.value, name.value, None]

    @property
    def pretty_signature(self):
        kw, name, args = self.signature()

        sig = f"({kw} {name} "
        if args is None:
            sig += "<value>)"
        elif kw not in self.macro_keywords:
            sig += f"(fun ({' '.join(args)}) (...)))"
        else:
            sig += f"({' '.join(args)}) (...))"
        return sig

    @property
    def defined_at(self):
        return deep_flatten(self.target[:])[0].line

    def __str__(self):
        return f"Documentation({len(self.comments)} comments, {self.pretty_signature}, line={self.defined_at})"
