from gevent.monkey import patch_all
patch_all()

import os
import sys
sys.path.append(os.path.abspath('.'))

import time
import traceback

import gevent
from gevent.pool import Pool
from importlib import import_module
from slackclient import SlackClient
from slacker import Slacker

from settings import APPS, CMD_PREFIX, CMD_LENGTH, MAX_WORKERS, SLACK_TOKEN
from chromedriver import ChromeDriver
from logger import getLogger


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
    if CMD_PREFIX and CMD_PREFIX != text[0]:
        return None, None

    tokens = text.split(' ', 1)
    if 1 < len(tokens):
        return tokens[0][CMD_LENGTH:], tokens[1]
    else:
        return text[CMD_LENGTH:], ''


def load_apps():
    docs = ['=' * 14, 'Usage', '=' * 14]
    apps = {}

    for name in APPS:
        app = import_module('apps.%s' % name)
        docs.append('`{0}{1}` {2}'.format(
            CMD_PREFIX, ', '.join(app.run.commands), app.run.__doc__
        ))
        for command in app.run.commands:
            apps[command] = app

    return apps, docs


class Robot(object):
    def __init__(self):
        self.logger = getLogger()
        self.client = SlackClient(SLACK_TOKEN)
        self.slacker = Slacker(SLACK_TOKEN)
        self.apps, self.docs = load_apps()
        self.chrome = ChromeDriver(self)
        self.pool = Pool(MAX_WORKERS)

    def handle_message(self, message):
        channel, user, text = message

        command, payloads = extract_command(text)
        if not command:
            return

        app = self.apps.get(command, None)
        if not app:
            return

        try:
            self.pool.apply_async(func=app.run,
                                  args=(self, channel, user, payloads))
        except:
            self.logger.error(traceback.format_exc())

    def rtm_connect(self):
        while not self.client.rtm_connect(with_team_state=False):
            self.logger.info('RTM Connecting...')
            time.sleep(1)
        self.logger.info('RTM Connected.')

    def read_message(self):
        try:
            return self.client.rtm_read()
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            self.logger.error(traceback.format_exc())
            self.rtm_connect()

    def run(self):
        self.rtm_connect()
        if not self.client.server.connected:
            raise RuntimeError(
                'Can not connect to slack client. Check your settings.'
            )

        while True:
            events = self.read_message()
            if events:
                self.logger.info(events)
                messages = extract_messages(events)
                for message in messages:
                    self.handle_message(message)
            gevent.sleep(0.3)

    def disconnect(self):
        if self.client and self.client.server and self.client.server.websocket:
            self.client.server.websocket.close()
        self.logger.info('RTM disconnected.')


if '__main__' == __name__:
    print('Initialize Robot Start...')
    robot = Robot()
    try:
        robot.run()
        robot.logger.info('Initialize Robot Complete...')
    except KeyboardInterrupt as e:
        robot.logger.info('Honey Shutdown By User.')
    finally:
        robot.disconnect()
        robot.logger.info('Honey Shutdown.')
        traceback.print_exc(file=sys.stdout)
