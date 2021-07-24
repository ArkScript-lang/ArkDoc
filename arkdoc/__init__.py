#!/usr/bin/env python3

from .logger_utils import Logger, LogLevel

import os
logger = Logger("ArkDoc", level=LogLevel[os.environ.get("ARKDOC_LOGLEVEL", "INFO")])

from .parser import Parser
from .reader import parse_all_in
