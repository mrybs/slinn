import datetime
import enum
import sys
from typing import IO


class LogLevel(enum.Enum):
    """
    Types of log. If logger`s log level higher than message`s log level, nothing will be logged
    """
    info = 0
    warning = 1
    error = 2
    critical = 3


class Logger:
    """
    Class for logging into stdout
    """
    def __init__(self, min_log_level: LogLevel, out: IO = sys.stdout) -> None:
        self.min_log_level = min_log_level
        self.out = out

    def __call__(self, log_level: LogLevel, message: str) -> bool:
        if log_level.value > self.min_log_level.value:
            self.out.write(f'[{log_level.name}] "{message}" at {datetime.datetime.now()}')
            self.out.flush()
            return True
        return False
