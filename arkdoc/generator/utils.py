#!/usr/bin/env python3

import re

from . import specification as spec
from ..parser import Documentation


def documentation_to_specification(doc: Documentation) -> spec.Function:
    _, name, *args = doc.signature()

    data = {
        'brief': '',
        'details': '',
        'params': [],
        'code': '',
        'author': []
    }

    for comment in doc.comments:
        for key in data:
            tag = f"@{key}"

            if tag in comment:
                res = re.sub(fr'#+ *{tag}', '', comment).strip()

                if isinstance(data[key], list):
                    data[key].append(res)
                else:
                    data[key] = res

    if len(data['params']) != len(args):
        raise ValueError(
            f"Function {name} was defined with {len(args)} arguments, "
            f"but only {len(data['params'])} are documented"
        )

    for i, param in enumerate(data['params']):
        param_name, desc = param.split(' ', 1)
        data['params'][i] = spec.Param(param_name, desc)

    return spec.Function(
        name,
        spec.Description(
            data["brief"],
            data["details"],
            data["params"],
            data["code"],
            data["author"]
        )
    )
