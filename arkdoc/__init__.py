#!/usr/bin/env python3

from .logger_utils import Logger, LogLevel

logger = Logger("ArkDoc", level=LogLevel.INFO)

from .parser import Parser
from .reader import parse_all_in
