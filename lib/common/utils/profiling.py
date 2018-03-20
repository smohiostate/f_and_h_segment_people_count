# Attribution:
# https://www.huyng.com/posts/python-performance-analysis

from functools import wraps
import time

from common.utils.monitoring import get_logger

class ExecutionTimer:

    def __init__(self, verbose=False, logging_facility=None):
        # If logging_facility is set, we will attempt to
        # use that logging facility to print verbose statements.
        self.verbose = verbose
        self.logging_facility = logging_facility

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000

        execution_time_str = self.execution_time_string()
        if self.logging_facility is not None:
            self.print_with_logging_facility(execution_time_str)
        elif self.verbose:
            self.print_with_print(execution_time_str)

    def print_with_logging_facility(self, statement):
        try:
            if self.verbose:
                self.logging_facility.info(statement)
            else:
                self.logging_facility.debug(statement)
        except AttributeError:
            print('Timer logging_facility was not initialized correctly. Defaulting to verbose print.')
            self.print_with_print(statement)

    def print_with_print(self, statement):
        print(statement)


    def execution_time_string(self):
        return 'Execution time: {} ms'.format(self.msecs)


def time_execution(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        logger = get_logger(f.__name__)
        with ExecutionTimer(verbose=True, logging_facility=logger):
            rv = f(*args, **kwargs)
        return rv

    return wrapper


