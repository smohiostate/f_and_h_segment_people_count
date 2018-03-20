import logging
import sys

from os import environ

DEFAULT_LOG_FORMAT = '%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] [%(name)s]  %(message)s'


def get_logger(name, log_format=DEFAULT_LOG_FORMAT, log_file=None, debug=environ.get('DEBUG_MODE', False) == 'True'):

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    # Logging setup, we are writing to stdout and our LOG_FILE
    log_formatter = logging.Formatter(log_format)

    if log_file is not None:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(log_formatter)
        logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)

    logger.addHandler(console_handler)

    return logger
