#!/usr/bin/env python3

import re
from typing import List, Any, Generator
from dataclasses import dataclass


@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int

    def __str__(self):
        return (
            f"Token({self.type}, '{self.value}', line={self.line}, col={self.column})"
        )


Keywords = "let mut set del fun if while import begin".split()
TokenSpecification = [
    ("NUMBER", r"\d+(\.\d*)?"),
    ("STRING", r"\"(\\\\|\\\"|[^\"])*\""),
    ("ID", r"[\w:?=!@&<>+\-%*/.$]+"),
    ("LPAREN", r"[(\[{]"),
    ("RPAREN", r"[)\]}]"),
    ("COMMENT", r"#[^\n]*"),
    ("EMPTY_LINE", r"\n\n"),
    ("NEWLINE", r"\n"),
    ("SKIP", r"[ \t]+"),
    ("MISMATCH", r"."),
]


def tokenize(code: str) -> Generator[Token, Any, None]:
    tok_regex = "|".join("(?P<%s>%s)" % pair for pair in TokenSpecification)
    line_num = 1
    line_start = 0

    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start

        if kind == "ID" and value in Keywords:
            kind = value
        elif kind == "NEWLINE":
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == "EMPTY_LINE":
            line_start = mo.end()
            line_num += 2
        elif kind == "SKIP":
            continue
        elif kind == "MISMATCH":
            lines = code.split("\n")
            raise RuntimeError(
                f"{value!r} unexpected on line {line_num}\n{lines[line_num - 1]}"
            )
        yield Token(kind, value, line_num, column)


"""
The following regex accepts this kind of comment

/**
  * test 
 * test
* test
  * @brief test
*/
"""
CPP_COMMENT_REGEX = r"^ */\*\*\n( *\*( *.*)\n)+"

"""
The following regex accepts this kind of text blocks

--#
* test
* test
* test
* @brief test
#--
"""
TXT_COMMENT_REGEX = r"^ *--#\n(\*( .*)\n)+#--\n"


def generic_tokenizer(regex: str, code: str) -> Generator[list[Token], Any, None]:
    line_num = 1
    line_start = 0

    def transform(line: str):
        nonlocal line_num
        lines = line.split("\n")

        for e in lines[1:]:
            line = "#" + e.strip()[1:]
            line_num += 1
            yield Token("COMMENT", line, line_num, column)

    for mo in re.finditer(regex, code, flags=re.MULTILINE):
        value = mo.group()
        column = mo.start() - line_start
        yield list(transform(value))


def tree_from_tokens(tokens: List[Token]) -> List:
    if len(tokens) == 0:
        raise SyntaxError("unexpected EOF")

    token = tokens.pop(0)

    L = []
    while token.type == "COMMENT":
        L.append(token)
        if not tokens:
            return L
        token = tokens.pop(0)

    if token.type == "LPAREN":
        L2 = []
        last_token = tokens[0]
        while tokens[0].type != "RPAREN":
            if not tokens:
                raise SyntaxError(f"No more tokens after {last_token}")
            L2 += [tree_from_tokens(tokens)]
        tokens.pop(0)
        L.append(L2)
        return L
    elif token.type == "RPAREN":
        raise SyntaxError(f"unexpected ) on line {token.line}, at {token.column}")
    elif token.type == "EMPTY_LINE":
        L.append(token)
        return L
    else:
        return token
