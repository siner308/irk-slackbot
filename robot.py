# coding: utf-8
from __future__ import unicode_literals

import sys
import gevent
import traceback

from gevent.pool import Pool
from importlib import import_module
from slackclient import SlackClient
from slacker import Slacker
from gevent.monkey import patch_all

from chromedriver import ChromeDriver
from settings import APPS, SLACK_TOKEN, POOL_SIZE
from logger import get_logger

patch_all()
pool = Pool(POOL_SIZE)
CMD_PREFIX = '!'
logger = get_logger('irk')


def load_apps():
    docs = ['=' * 14, 'Usage', '=' * 14]
    apps = {}

    for name in APPS:
        app = import_module('functions.%s' % name)
        docs.append(
            '!%s: %s' % (', '.join(app.run.commands), app.run.__doc__)
        )
        for command in app.run.commands:
            apps[command] = app

    return apps, docs


def extract_messages(events):
    messages = []
    for event in events:
        channel = event.get('channel', '')
        user = event.get('user', '')
        text = event.get('text', '')
        if channel and user and text:
            messages.append((channel, user, text))
    return messages


def extract_command(text):
    if CMD_PREFIX != text[0]:
        return None, None

    tokens = text.split(' ', 1)
    if 1 < len(tokens):
        return tokens[0][1:], tokens[1]
    else:
        return text[1:], ''


class Robot(object):
    def __init__(self):
        self.client = SlackClient(SLACK_TOKEN)
        self.slacker = Slacker(SLACK_TOKEN)
        self.chrome = ChromeDriver()
        self.apps, self.docs = load_apps()

    def handle_message(self, message):
        channel, user, text = message

        command, payloads = extract_command(text)
        if not command:
            return

        app = self.apps.get(command, None)
        if not app:
            return

        try:
            pool.apply_async(func=app.run,
                             args=(self, channel, user, payloads))
        except:
            traceback.print_exc()

    def rtm_connect(self):
        try:
            conn = self.client.rtm_connect()
        except:
            logger.error(traceback.format_exc())
        else:
            return conn

    def read_message(self):
        events = None
        try:
            events = self.client.rtm_read()
        except:
            self.rtm_connect()
        return events

    def run(self):
        if not self.rtm_connect():
            raise RuntimeError('Can not connect to slack client. Check your settings.')

        while True:
            events = self.read_message()
            if events:
                logger.info(events)
                messages = extract_messages(events)
                for message in messages:
                    self.handle_message(message)
            gevent.sleep(0.3)


if '__main__' == __name__:
    try:
        print('Initialize Robot Start...')
        robot = Robot()
        print('Initialize Robot Complete...')
        robot.run()
    except:
        traceback.print_exc(file=sys.stdout)
