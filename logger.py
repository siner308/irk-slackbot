import sys
import logging
from settings import TEST


def getLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if TEST:
        handler = logging.StreamHandler(sys.stdout)
    else:
        handler = logging.FileHandler('honey.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)
    return logger

