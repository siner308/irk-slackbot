# coding: utf-8
import os


try:
    test = os.environ['TEST']
except:
    test = None

if test:
    SLACK_TOKEN = 'test_token'
    CHANNEL = '#test_channel'
else:
    SLACK_TOKEN = 'prod_token'
    CHANNEL = '#prod_channel'

BOT_NAME = 'bot_name'
REDIS_URL = None

MONGO_HOST = '123.456.789.012'
MONGO_PORT = 12345
MONGO_DATABASE = 'db_name'

# gevent pool size
POOL_SIZE = 20

# add your app name to this list
APPS = [
    'calc_hack_cooltime',
    'calc_link_distance',
    'get_intel_screenshot',
]
