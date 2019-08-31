# coding: utf-8
from __future__ import unicode_literals
import pymongo
import datetime
from functions.decorators import on_command
from gevent.monkey import patch_all
from slack import slack_notify

patch_all()


@on_command(['인텔'])
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

    if worktime is not None:
        text = "어디서 출근도 안하고 퇴근을!!!"
    else:
        end_time = datetime.datetime.now()
        worktime = end_time - data['start_time']
        value = {"$set": {"end_time": end_time, 'worktime': str(worktime)}}
        key = {"_id": data['_id']}
        try:
            coll.update_one(key, value)
            text = "[%s] - 퇴근 - %s\n`%s` 만큼 일했습니다." % (str(end_time), data['_id'], str(worktime))
        except Exception as e:
            text = str(e)
            fallback = '고장났어!!!'

    attachments_dict['fallback'] = fallback
    attachments_dict['text'] = text
    attachments = [attachments_dict]
    slack_message = None
    slack_notify(slack_message, channel, username='fluxbot', attachments=attachments)
