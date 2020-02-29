# coding: utf-8
from __future__ import unicode_literals
from decorators import on_command

import requests
from bs4 import BeautifulSoup as Soup


URL = 'http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=1162057500'


@on_command(['ㅇㄷ', '온도', '더워'])
def run(robot, channel, user, tokens):
    '''현재 시간의 온도를 알려드립니다.'''
    res = requests.get(URL).text
    soup = Soup(res, features='xml')
    data = soup.body.find_all('data')
    for each in data:
        cur_temp = each.temp.text
        if float(cur_temp) >= 30:
            return channel, '현준씨 벌써 %s 도에요 에어컨좀 틀어주세요.' % (cur_temp)
        else:
            return channel, '현재의 온도는 %s도 입니다. ' % (cur_temp)

    return channel, '온도 확인 접속 실패. 잠시 후 다시 시도해주세요!'
