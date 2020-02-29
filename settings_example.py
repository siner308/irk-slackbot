import os

# # # # # # # # # # # #
# Honey Configuration #
# # # # # # # # # # # #

# command prefix
CMD_PREFIX = '!'
CMD_LENGTH = len(CMD_PREFIX)

# number of workers
MAX_WORKERS = 20

# add your app name to this list
APPS = [
    # 'calc_hack_cooltime',
    'calc_link_distance',
    'ingress_intel',
    'helper',
    # 'giphy',
]

# # # # # # # # # # # #
# Siner Configuration #
# # # # # # # # # # # #
try:
    TEST = os.environ['TEST']
except:
    TEST = None

if TEST:
    SLACK_TOKEN = ''
    CHANNEL = ''
    SERVER_URL = ''
    LOG_DIR = './'
else:
    SLACK_TOKEN = ''
    CHANNEL = ''
    SERVER_URL = ''
    LOG_DIR = ''

STATIC_ROOT = '/var/www/html'
CHROMEDRIVER_PATH = os.path.dirname(os.path.realpath(__file__)) + '/chromedriver'
# CHROMEDRIVER_PATH = './chromedriver'

# Slack
BOT_NAME = ''
ZABGRESS_ICON_URL = ''
GIPHY_ICON_URL = ''

# Ingress
GOOGLE_EMAIL = ''
GOOGLE_PASSWORD = ''
INGRESS_AGENT_NAME = ''
GOOGLE_MAP_KEY = ''

# Giphy
GIPHY_KEY = ''

# MongoDB
MONGO_HOST = ''
MONGO_PORT = 21025
MONGO_DATABASE = ''

# Color
RED = '#FF0000'
GREEN = '#008000'
ORANGE = '#FFA500'

