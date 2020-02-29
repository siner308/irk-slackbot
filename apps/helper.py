from . import on_command


@on_command(['명령어'])
def run(robot, channel, user, tokens):
    '''도움말을 출력해드려요'''
    robot.slacker.chat.post_message(channel=channel, text='\n'.join(robot.docs))
