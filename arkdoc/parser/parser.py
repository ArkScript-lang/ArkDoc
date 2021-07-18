#!/usr/bin/env python3

import re
from typing import List, NamedTuple

from .. import logger


class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int

    def __str__(self):
        return f"Token({self.type}, '{self.value}', line={self.line}, col={self.column})"


Keywords = "let mut set del fun if while import begin quote".split()
TokenSpecification = [
    ('NUMBER', r'\d+(\.\d*)?'),
    ('STRING', r'"[^"]*"'),
    ('ID', r'[\w:?=!@&<>+\-%*/.]+'),
    ('LPAREN', r'[(\[{]'),
    ('RPAREN', r'[)\]}]'),
    ('COMMENT', r'#[^\n]*'),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
    ('MISMATCH', r'.'),
]


def tokenize(code: str) -> List[Token]:
    tok_regex = '|'.join(
        '(?P<%s>%s)' %
        pair for pair in TokenSpecification
    )
    line_num = 1
    line_start = 0

    lines = code.split('\n')

    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start

        if kind == 'ID' and value in Keywords:
            kind = value
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(
                f'{value!r} unexpected on line {line_num}\n{lines[line_num - 1]}'
            )
        yield Token(kind, value, line_num, column)



def tree_from_tokens(tokens: List[Token]) -> List:
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')

    token = tokens.pop(0)

    L = []
    while token.type == 'COMMENT':
        L.append(token)
        token = tokens.pop(0)

    if token.type == 'LPAREN':
        L2 = []
        while tokens[0].type != 'RPAREN':
            L2.append(tree_from_tokens(tokens))
        tokens.pop(0)
        L.append(L2)
        return L
    elif token.type == 'RPAREN':
        raise SyntaxError(f"unexpected ) on line {token.line}, at {token.column}")
    else:
        return token


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

    def parse(self):
        with open(self.filename, 'r') as f:
            program = f.read()

        self.ast = tree_from_tokens(list(tokenize(program)))
        self.visit(self.ast)
