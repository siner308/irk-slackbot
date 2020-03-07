import sys
import logging
from settings import TEST, LOG_DIR


def getLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if TEST:
        handler = logging.StreamHandler(sys.stdout)
    else:
        handler = logging.FileHandler('%s/honey.log' % LOG_DIR)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)
    return logger

