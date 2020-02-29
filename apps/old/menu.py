# coding: utf-8
from __future__ import unicode_literals
from decorators import on_command

import requests
import random

@on_command(['오늘뭐먹지', '메뉴추천', "점심", "배고파", 'menu'])
def run(robot, channel, user, tokens):
    '''오늘의 점심 메뉴'''
    with open('./apps/menu.list', 'r') as file:
        menus = file.read().splitlines()
    length = len(menus)
    R = random.Random()
    idx = R.randrange(1, length)
    return channel, "오늘의 점심 메뉴!!! %s"%unicode(menus[idx], "utf-8")

