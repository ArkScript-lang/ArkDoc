#!/usr/bin/env python3

import re
from typing import Tuple, Dict
from copy import deepcopy

from . import specification as spec
from ..parser import Documentation, Source
from .. import logger

DEFAULT_KEYS = {
    "brief": "",
    "details": "",
    "param": [],
    "author": "",
    "deprecated": "",
    "changed": []
}


def extractor(data: Dict, doc: Documentation) -> Tuple[Dict, str]:
    in_code = False
    code = []

    for comment in doc.comments:
        if not in_code:
            for key in data:
                tag = f"@{key}"

                if tag in comment.value:
                    res = re.sub(fr"#+ *{tag}", "", comment.value).strip()

                    if res:
                        if isinstance(data[key], list):
                            data[key].append(res)
                        else:
                            data[key] = res
            else:
                if "=begin" in comment.value:
                    in_code = True
        else:
            if "=end" not in comment.value:
                code.append(comment.value)
            else:
                in_code = False

    if code:
        margin = code[0].index("(")
        code = [line[margin:] for line in code]

    if "param" in data:
        for i, param in enumerate(data["param"]):
            param_name, desc = param.split(" ", 1)
            data["param"][i] = spec.Param(param_name, desc)
    if "changed" in data:
        for i, changed in enumerate(data["changed"]):
            version, desc = changed.split(" ", 1)
            data["changed"][i] = spec.Change(version, desc)
    if "author" in data:
        data["author"] = [el.strip() for el in data["author"].split(",") if data["author"]]

    return data, "\n".join(code)


def describe(data: Dict, code: str) -> spec.Description:
    return spec.Description(
        brief=data["brief"],
        details=data["details"],
        params=data["param"],
        code=code,
        authors=data["author"],
        deprecation_notice=data["deprecated"],
        changelist=data["changed"]
    )


def from_ark(doc: Documentation) -> spec.Function:
    _, name, args = doc.signature()
    data, code = extractor(deepcopy(DEFAULT_KEYS), doc)

    if args is not None and len(data["param"]) != len(args):
        logger.warn(
            f"Function {name} was defined with {len(args)} argument(s), "
            f"but {len(data['param'])} are documented"
        )

    return spec.Function(
        name,
        doc.pretty_signature,
        describe(data, code),
    )


def from_cpp(doc: Documentation) -> spec.Function:
    parameters = {"name": ""}
    parameters.update(deepcopy(DEFAULT_KEYS))
    data, code = extractor(parameters, doc)

    return spec.Function(
        data["name"],
        f"Builtin ({data['name']} {' '.join(e.name for e in data['param'])})",
        describe(data, code),
    )


def documentation_to_specification(doc: Documentation) -> spec.Function:
    if doc.source == Source.ArkScript:
        return from_ark(doc)
    elif doc.source == Source.Cpp:
        return from_cpp(doc)
    else:
        raise NotImplementedError
