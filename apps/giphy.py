
# coding: utf-8
from __future__ import unicode_literals
from . import on_command

# from gevent.monkey import patch_all
# patch_all()

import re
import random
import requests
from urllib import parse
from settings import CHANNEL, GIPHY_ICON_URL, GIPHY_KEY


HELP_MSG = [
    'giphy 에서 움짤을 검색하고 싶으면 \'!움짤 [검색어]\' 이라고 해주세요.',
    '검색어는 `영어`만 됩니다. 검색어에 띄어쓰기가 들어있다면 큰따옴표로 감싸주세요.',
]

URL = 'http://api.giphy.com/v1/gifs/search?'


def get_giphy_image_url(query):
    params = {
        'q': query,
        'api_key': GIPHY_KEY,
        'offset': random.randint(0, 100),
        'limit': 1,
    }
    data = requests.get(URL, params=params).json()

    if data['pagination']['count'] < 1:
        return None
    else:
        el = data['data'][0]
        return el['images']['downsized']['url']
        #return el['images']['preview_gif']['url']
        #return el['images']['original']['url']


def check_korean(query):
    return re.search(r'[ㄱ-ㅎㅏ-ㅣ가-힣]', query, re.U)


@on_command(['ㄱㅍ', '움짤', 'gif', 'giphy'])
def run(robot=None, channel=None, user=None, tokens=None):
    if not channel:
        channel = CHANNEL
    is_success = True
    image_url = 'https://media.giphy.com/media/nR4L10XlJcSeQ/giphy.gif'
    attachments_dict = dict()
    attachments_dict['fallback'] = '움직인당'
    attachments_dict['mrkdwn_in'] = ['text']
    slack_message = None

    '''Search a random image from giphy.com.'''
    tokens = list(tokens)
    if not len(tokens):
        is_success = False
        text = 'giphy 에서 움짤을 검색하고 싶으면 *!움짤 [검색어]* 이라고 해주세요.' \
               '검색어는 `영어`만 됩니다. 검색어에 띄어쓰기가 들어있다면 큰따옴표로 감싸주세요.'
    else:
        query = ' '.join(tokens)
        print(query)

    if is_success and check_korean(query):
        is_success = False
        text = '`영어만 가능합니다` :gzrn:'

    if is_success:
        response = get_giphy_image_url(query)
        image_url = response if response else image_url

    if is_success:
        text = parse.unquote(query)

    attachments_dict['text'] = text
    attachments_dict['image_url'] = image_url
    attachments = [attachments_dict]
    robot.slacker.chat.post_message(text=slack_message, channel=channel, username='giphy', attachments=attachments,
                                    icon_url=GIPHY_ICON_URL)


# if '__main__' == __name__:
#     print get_giphy_message('funny cat')
