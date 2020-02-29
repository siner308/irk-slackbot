# coding: utf-8
from __future__ import unicode_literals
import pymongo
import datetime
from . import on_command
from gevent.monkey import patch_all
from slack import slack_notify

patch_all()


@on_command(['출근', '출근!', '출근!!', '출근!!!',
             '일할게', '일할게!', '일할게!!', '일할게!!!',
             'ㅊㄱ', 'ㅊㄱ!', 'ㅊㄱ!!', 'ㅊㄱ!!!'])
def run(robot, channel, user, tokens):
    fallback = '출퇴근봇알리미'
    attachments_dict = dict()

    dbclient = pymongo.MongoClient("192.168.1.123", 27017)
    db = dbclient['fluxbot']
    coll = db['commute']

    key = {"user": user}
    rows = list(coll.find(key).sort('_id', pymongo.DESCENDING))
    data = rows[0]

    try:
        worktime = data['worktime']
    except:
        worktime = None

    if worktime is None:
        text = "어디서 퇴근도 안하고 출근을!!!"
    else:
        start_time = datetime.datetime.now()
        data = {"user": user, "start_time": start_time}
        try:
            x = coll.insert_one(data)
            text = "[%s] - 출근 - %s" % (str(start_time), x.inserted_id)
        except Exception as e:
            text = str(e)
            fallback = '고장났어!!!'

    attachments_dict['fallback'] = fallback
    attachments_dict['text'] = text
    attachments = [attachments_dict]
    slack_message = None
    slack_notify(slack_message, channel, username='fluxbot', attachments=attachments)
