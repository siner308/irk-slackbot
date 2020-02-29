from slacker import Slacker
from settings import SLACK_TOKEN, CHANNEL, BOT_NAME


def slack_notify(text=None, channel=None, username=None, attachments_dict=None, icon_url=None):
    slack = Slacker(SLACK_TOKEN)
    if not username:
        username = BOT_NAME
    if not CHANNEL:
        channel = CHANNEL
    attachments = [attachments_dict]
    slack.chat.post_message(text=text, channel=channel, username=username, attachments=attachments, icon_url=icon_url)

