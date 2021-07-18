#!/usr/bin/env python3

from typing import List
from collections import OrderedDict

from .. import logger


class Symbol(str):
    pass


class Comment(str):
    pass


Keywords = "let mut set del fun if while import begin quote".split()
Number = (int, float)
Atom = (Comment, Symbol, Number)


class Parser:
    def __init__(self, filename: str):
        self.filename = filename
        self.ast = None

    def _tokenize(self, chars: str) -> List[str]:
        transformations = OrderedDict([
            ('\n', ' '),
            ('\r', ' '),
            ('\t', ' '),
            ('{', '(begin'),
            ('}', ')'),
            ('[', '(list'),
            (']', ')'),
            ('(', ' ( '),
            (')', ' ) '),
        ])

        for before, after in transformations.items():
            chars = chars.replace(before, after)

        return chars.split(' ')

    def _read_from_tokens(self, tokens: List[str]) -> List:
        if len(tokens) == 0:
            raise SyntaxError('unexpected EOF')

        token = tokens.pop(0)

        if token == '(':
            L = []
            while tokens[0] != ')':
                L.append(self._read_from_tokens(tokens))

            tokens.pop(0)  # pop off ')'
            return L
        elif token == ')':
            raise SyntaxError('unexpected )')
        else:
            return self._atom(token)

    def _atom(self, token: str) -> Atom:
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                if token and token[0] == '#':
                    return Comment(token)
                else:
                    return Symbol(token)

    def parse(self):
        with open(self.filename, 'r') as f:
            program = f.read()

        self.ast = self._read_from_tokens(self._tokenize(program))
        logger.debug(self.ast)
