import logging
import sys


class IndentFormatter(logging.Formatter):
    def format(self, record):
        original = super().format(record)
        lines = original.splitlines()
        return '\n'.join([lines[0]] + [f'    {line}' for line in lines[1:]])


def setup_logging(level: int = logging.INFO):
    fmt = '%(asctime)s %(levelname)-7s %(filename)s:%(lineno)d — %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(IndentFormatter(fmt=fmt, datefmt=datefmt))

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers = [handler]
