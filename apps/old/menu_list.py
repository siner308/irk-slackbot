# coding: utf-8
from __future__ import unicode_literals
from decorators import on_command

import requests


@on_command(['점심리스트', '점심목록', 'menu_list'])
def run(robot, channel, user, tokens):
    '''점심 메뉴 리스트'''
    with open('./apps/menu.list', 'r') as file:
        menus = file.read().splitlines()
        
    message = ""
    for menu in menus:
        message += "%s, "%unicode(menu, "utf-8")

    return channel, "오늘의 점심 목록!!!\n%s"%message

