import logging


class CustomDebugFormatter(logging.Formatter):
    COLOR_CODES = {
        "red": "\033[1;91m",
        "green": "\033[1;92m",
        "yellow": "\033[1;93m",
        "blue": "\033[1;94m",
        "cyan": "\033[1;96m",
        "purple": "\033[1;95m",
        "reset": "\033[0m",
    }

    def __init__(self, debug_color, fmt=None, datefmt=None):
        super().__init__(fmt, datefmt)
        self.debug_color = debug_color

    def format(self, record):
        if record.levelno == logging.DEBUG:
            record.msg = f"{self.COLOR_CODES[self.debug_color]}{record.msg}\033[0m"
        return super().format(record)

    @staticmethod
    def create_logger(name, debug_color):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        formatter = CustomDebugFormatter(
            debug_color, fmt="%(message)s"
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger
