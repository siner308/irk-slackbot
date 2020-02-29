import os
import sys
sys.path.append(os.path.abspath('.'))

import time
import traceback
from importlib import import_module
from slackclient import SlackClient
from slacker import Slacker
from concurrent.futures import ThreadPoolExecutor, TimeoutError

from settings import APPS, CMD_PREFIX, CMD_LENGTH, MAX_WORKERS, SLACK_TOKEN
from chromedriver import ChromeDriver
from logger import log_or_print


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
        docs.append('{0}{1}: {2}'.format(
            CMD_PREFIX, ', '.join(app.run.commands), app.run.__doc__
        ))
        for command in app.run.commands:
            apps[command] = app

    return apps, docs


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
            app.run(self, channel, user, payloads)
        except:
            log_or_print(traceback.format_exc())

    def rtm_connect(self):
        while not self.client.rtm_connect(with_team_state=False):
            log_or_print('RTM Connecting...')
            time.sleep(1)
        log_or_print('RTM Connected.')

    def read_message(self):
        try:
            return self.client.rtm_read()
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            log_or_print(traceback.format_exc())
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
                messages = extract_messages(events)
                if messages:
                    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                        try:
                            executor.map(self.handle_message, messages)
                        except TimeoutError:
                            log_or_print(traceback.format_exc())
            else:
                time.sleep(0.3)

    def disconnect(self):
        if self.client and self.client.server and self.client.server.websocket:
            self.client.server.websocket.close()
        log_or_print('RTM disconnected.')


if '__main__' == __name__:
    print('Initialize Robot Start...')
    robot = Robot()
    try:
        robot.run()
        print('Initialize Robot Complete...')
    except KeyboardInterrupt as e:
        log_or_print('Honey Shutdown By User.')
    finally:
        robot.disconnect()
        log_or_print('Honey Shutdown.')
        traceback.print_exc(file=sys.stdout)
