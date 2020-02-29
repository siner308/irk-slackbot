# import logging
# from datetime import datetime
# from settings import LOG_DIR, TEST

import logging

level = logging.DEBUG
logger = logging.getLogger('irk')
logger.setLevel(level)

log_file_handler = logging.FileHandler('honey.log')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
log_file_handler.setFormatter(formatter)
logger.addHandler(log_file_handler)
#
# def get_logger(key):
#     _logger = logging.getLogger(key)
#     _logger.setLevel(logging.INFO)
#
#     log_file_handler = logging.FileHandler(LOG_DIR + '%s.log' % key)
#     formatter = logging.Formatter(
#         '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#     )
#     log_file_handler.setFormatter(formatter)
#     _logger.addHandler(log_file_handler)
#
#     return _logger
#
#
# logger = get_logger('irk')
#
#
# def log_or_print(message):
#     now = datetime.now().strftime('%F %H:%M:%S')
#
#     message_with_time = '[%s] %s' % (now, message)
#     if TEST:
#         print(message_with_time)
#     else:
#         logger.info(message_with_time)
#
