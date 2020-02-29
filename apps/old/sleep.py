# coding: utf-8
from __future__ import unicode_literals
from decorators import on_command

import requests
from bs4 import BeautifulSoup as Soup


URL = 'http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=1162057500'


@on_command(['졸려', '잠와', 'sleep'])
def run(robot, channel, user, tokens):
    '''넘나 졸려요....'''
    return channel, '커피 한잔 고고?? 눈치게임 1!' 

