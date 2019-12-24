import logging
from settings import LOG_DIR


def get_logger(key):
    logger = logging.getLogger(key)
    logger.setLevel(logging.INFO)

    log_file_handler = logging.FileHandler(LOG_DIR + '%s.log' % key)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    log_file_handler.setFormatter(formatter)
    logger.addHandler(log_file_handler)

    return logger
