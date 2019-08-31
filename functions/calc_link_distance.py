# coding: utf-8
from __future__ import unicode_literals

from functions.decorators import on_command
from gevent.monkey import patch_all
from slack import slack_notify

from settings import CHANNEL

patch_all()

table = {
    '': 1.000,
    'R': 2.000,
    'RR': 2.500,
    'RRR': 2.750,
    'RRRR': 3.000,
    'S': 5.000,
    'SR': 5.500,
    'SRR': 5.750,
    'SRRR': 6.000,
    'SS': 6.250,
    'SSR': 6.500,
    'SSRR': 6.750,
    'SSS': 6.825,
    'SSSR': 7.125,
    'SSSS': 7.500,
    'V': 7.000,
    'VR': 7.500,
    'VRR': 7.750,
    'VRRR': 8.000,
    'VS': 8.250,
    'VSR': 8.500,
    'VSRR': 8.750,
    'VSS': 8.875,
    'VSSR': 9.125,
    'VSSS': 9.500,
    'VV': 8.750,
    'VVR': 9.000,
    'VVRR': 9.250,
    'VVS': 9.375,
    'VVSR': 9.625,
    'VVSS': 10.000,
    'VVV': 9.625,
    'VVVR': 9.875,
    'VVVS': 10.250,
    'VVVV': 10.500,
}

@on_command(['링크', 'link'])
def run(robot, channel, user, tokens):
    icon_url = 'https://commondatastorage.googleapis.com/ingress.com/img/map_icons/marker_images/hum_reso_08.png'
    BOT_NAME = 'link-calculator'
    text = '고장났으면 신나를 외쳐!'
    is_success = True
    slack_message = None
    attachments_dict = dict()
    attachments_dict['fallback'] = BOT_NAME

    tokens = list(tokens)

    # send help information
    if not len(tokens):
        text = '*!링크 또는 !link* 명령어 입력 후, *레조조합*, *모드조합* 을 각각 띄어쓰기로 구분하여 적어주시면 됩니다.\n' \
               '>*V*: Very Rare Link Amp\n' \
               '>*S*: Softbank Link Amp\n' \
               '>*R*: Rare Link Amp\n' \
               'ex1) `!link 87665544 RR`\n' \
               'ex2) `!링크 8766 SSRR`'
        is_success = False

    if is_success:
        resonators = tokens[0]
        # select mod
        try:
            mods = ''.join(sorted(tokens[1].upper(), key=lambda m: {'V': 1, 'S': 2, 'R': 3}[m]))
        except:
            mods = ''

        try:
            power_of_mods = table[mods]
        except:
            text = '`모드가 잘못되었습니다.` (V,S,R 조합으로 최대 4개까지!)\n' \
                   '도움말은 `!링크` 또는 `!link`'
            is_success = False

    if is_success:
        # calc link distance
        try:
            distance = round(160 * ((sum(map(int, resonators)) / 8.0) ** 4) / 1000.0 * power_of_mods, 3)
        except:
            text = '`뭔가 실수했군요!?`\n' \
                   '도움말은 `!링크` 또는 `!link`'
            is_success = False

    if is_success:
        # reso count exception
        if len(resonators) < 8:
            text = '`레조네이터가 8개가 아닙니다. (8개보다 적으면 링크가 나가지 않아요)`\n' \
                   '도움말은 `!링크` 또는 `!link`'
        elif len(resonators) > 8:
            text = '`레조네이터가 8개가 아닙니다. (8개보다 적으면 링크가 나가지 않아요)`\n' \
                   '도움말은 `!링크` 또는 `!link`'
        else:
            # select notation
            if distance < 1:
                distance *= 1000
                text = '`%s m`' % distance
            else:
                text = '`%s km`' % distance

    attachments_dict['text'] = text
    attachments = [attachments_dict]
    slack_notify(text=slack_message, channel=CHANNEL, username=BOT_NAME, attachments=attachments, icon_url=icon_url)
