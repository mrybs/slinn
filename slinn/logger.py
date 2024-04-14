import enum, datetime

class LogLevel(enum.Enum):
    info = 0
    warning = 1
    error = 2
    critical = 3

class Logger:
    def __init__(self, min_log_level: LogLevel):
        self.min_log_level = min_log_level

    def __call__(self, log_level: LogLevel, message: str) -> bool:
        if log_level.value > self.min_log_level.value:
            print(f'[{log_level.name}] "{message}" at {datetime.datetime.now()}')
            return True
        return False