import functools
import logging
import os
import traceback


def safe_call(logger):
    def decorator_safe_call(func):
        @functools.wraps(func)
        def wrapper_safe_call(self, *args, **kwargs):
            if not callable(logger):
                raise Exception("The first argument must be a lambda")
            try:
                return func(self, *args, **kwargs)
            except Exception as err:
                exc = traceback.format_exception_only(type(err), err)
                logger(self).error(f'Unhandled Error: {exc} , STACK: {traceback.extract_stack()}')
                return None
        return wrapper_safe_call
    return decorator_safe_call


def create_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    log_file = os.path.join(os.path.dirname(__file__), f'{name}.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
