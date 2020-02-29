# coding: utf-8
from __future__ import unicode_literals

from . import on_command

from settings import RED, ORANGE, GREEN, ZABGRESS_ICON_URL


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
    '''레저네이터, 모드 상태에 따른 링크거리를 알려드려요'''
    BOT_NAME = 'link-calculator'
    text = '고장났으면 신나를 외쳐!'
    is_success = True
    slack_message = None
    attachments_dict = dict()
    attachments_dict['fallback'] = BOT_NAME
    attachments_dict['mrkdwn_in'] = ['text']

    tokens = list(tokens)

    # send help information
    if not len(tokens):
        text = '*!링크 또는 !link* 명령어 입력 후, *레조조합*, *모드조합* 을 각각 띄어쓰기로 구분하여 적어주시면 됩니다.\n' \
               '>*V*: Very Rare Link Amp\n' \
               '>*S*: Softbank Link Amp\n' \
               '>*R*: Rare Link Amp\n' \
               'ex1) `!link 87665544 RR` ex2) `!링크 8766 SSRR`'
        is_success = False
    elif len(tokens) == 1:
        has_mod = False
    else:
        has_mod = True

    # check resonator
    if is_success:
        resonators = list(tokens[0])
        reso_count = len(resonators)
        # reso count exception
        if reso_count > 8:
            text = '`레조네이터를 8개보다 많이 입력하였습니다.`\n' \
                   '도움말은 `!링크` 또는 `!link`'
            attachments_dict['color'] = RED
            is_success = False
        else:
            sum = 0
            for reso in resonators:
                try:
                    lv_reso = int(reso)
                except Exception as e:
                    robot.logger.warn(e)
                    robot.logger.warn(tokens)
                    is_success = False
                    text = '`레조네이터가 잘못되었습니다`'
                    attachments_dict['color'] = RED
                    break

                if lv_reso > 8:
                    text = '`레조네이터의 레벨 범위는 0부터 8입니다.`'
                    is_success = False
                    attachments_dict['color'] = RED
                    break
                else:
                    sum += lv_reso

    # check mod
    if is_success:
        if has_mod:
            try:
                mods = ''.join(sorted(tokens[1].upper(), key=lambda m: {'V': 1, 'S': 2, 'R': 3}[m]))
                power_of_mods = table[mods]
            except Exception as e:
                robot.logger.warn(e)
                robot.logger.warn(tokens)
                is_success = False
                text = '`모드가 잘못되었습니다.` (V,S,R 조합으로 최대 4개까지!)\n' \
                       '도움말은 `!링크` 또는 `!link`'
                attachments_dict['color'] = RED
        else:
            power_of_mods = 1

    # calc link distance
    if is_success:
        try:
            distance = round(160 * ((sum / 8.0) ** 4) * power_of_mods, 3)
        except Exception as e:
            robot.logger.warn(e)
            robot.logger.warn(tokens)
            is_success = False
            text = '`뭔가 실수했군요?!`\n' \
                   '도움말은 `!링크` 또는 `!link`'
            attachments_dict['color'] = RED

    # make message
    if is_success:
        attachments_dict['color'] = GREEN
        # select notation
        if distance > 1000:
            distance /= 1000
            text = '`%s km`' % distance
        else:
            text = '`%s m`' % distance

        if reso_count < 8:  # += 문법때문에 아래에 위치한 코드
            text += '\n`레조네이터가 8개보다 적으면 링크가 나가지 않아요`\n' \
                   '도움말은 `!링크` 또는 `!link`'
            attachments_dict['color'] = ORANGE

    attachments_dict['text'] = text
    attachments = [attachments_dict]
    robot.slacker.chat.post_message(text=slack_message, channel=channel, username=BOT_NAME, attachments=attachments,
                                    icon_url=ZABGRESS_ICON_URL)
