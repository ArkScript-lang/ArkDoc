#!/usr/bin/env python3

import colorama
from enum import Enum
from datetime import datetime


class LogLevel(Enum):
    DEBUG = 4
    INFO = 3
    WARN = 2
    ERROR = 1
    NONE = 0


class Logger:
    def __init__(self, name: str, level: LogLevel = LogLevel.NONE):
        self.name = name
        self.level = level

    def _print(self, kind: LogLevel, *args):
        colors = {
            LogLevel.DEBUG: colorama.Fore.MAGENTA,
            LogLevel.INFO: colorama.Fore.CYAN,
            LogLevel.WARN: colorama.Fore.YELLOW,
            LogLevel.ERROR: colorama.Fore.RED
        }

        if kind.value > self.level.value:
            return

        prefix = f"[{colors[kind]}{kind.name:^5}{colorama.Fore.RESET}]"
        now = datetime.now().isoformat(timespec='minutes')
        colored_now = f"{colorama.Fore.MAGENTA}{now}{colorama.Fore.RESET}"
        rest = ' '.join(str(el) for el in args)

        print(
            f"{prefix} -- {colored_now} -- {rest}"
        )

    def debug(self, *args):
        self._print(LogLevel.DEBUG, *args)

    def info(self, *args):
        self._print(LogLevel.INFO, *args)

    def warn(self, *args):
        self._print(LogLevel.WARN, *args)

    def error(self, *args):
        self._print(LogLevel.ERROR, *args)


colorama.init()
