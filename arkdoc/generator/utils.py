#!/usr/bin/env python3

import re

from . import specification as spec
from ..parser import Documentation
from .. import logger


def documentation_to_specification(doc: Documentation) -> spec.Function:
    _, name, *args = doc.signature()

    data = {
        'brief': '',
        'details': '',
        'param': [],
        'code': '',
        'author': []
    }

    for comment in doc.comments:
        for key in data:
            tag = f"@{key}"

            if tag in comment.value:
                res = re.sub(fr'#+ *{tag}', '', comment.value).strip()

                if isinstance(data[key], list):
                    data[key].append(res)
                else:
                    data[key] = res

    if len(data['param']) != len(args):
        logger.warn(
            f"Function {name} was defined with {len(args)} arguments, "
            f"but only {len(data['param'])} are documented"
        )

    for i, param in enumerate(data['param']):
        param_name, desc = param.split(' ', 1)
        data['param'][i] = spec.Param(param_name, desc)

    return spec.Function(
        name,
        doc.pretty_signature,
        spec.Description(
            data["brief"],
            data["details"],
            data["param"],
            data["code"],
            data["author"]
        )
    )
