import logging
import os


def create_logger(module_name):
    logger_instance = logging.getLogger(module_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger_instance.addHandler(handler)
    level = os.environ['LOG_LEVEL'].upper() if os.environ.get('LOG_LEVEL') else 'INFO'
    logger_instance.setLevel(level)
    return logger_instance


logger = create_logger('worker')
