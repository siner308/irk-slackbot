# python
import datetime
import time
from random import choice
from uuid import uuid4


# local
from . import on_command
from settings import ZABGRESS_ICON_URL, GIPHY_ICON_URL, CHANNEL, RED, ORANGE, GREEN, BOT_NAME, \
    MAX_LOAD_TIME
from apps.utils.google.maps import get_location
from apps.giphy import get_giphy_image_url


@on_command(['인텔', 'intel'])
def run(robot, channel, user, tokens):
    '''인텔 스크린샷 찍어드려요'''
    start_time = int(time.time())
    if not channel:
        channel = CHANNEL

    attachments_dict = dict()
    attachments_dict['fallback'] = BOT_NAME
    attachments_dict['mrkdwn_in'] = ['text']
    attachments_dict['text'] = '`고장났으면 신나를 외쳐!`'

    now = datetime.datetime.now()

    tokens = list(tokens)

    # send help information
    if not len(tokens):
        attachments_dict['text'] = '*!인텔 또는 !intel* 명령어 입력 후, 원하는 위치의 주소를 아는대로 적어주시면 됩니다.\n' \
                                   'ex1) `!인텔 해운대 해수욕장` ex2) `!intel 올림픽공원`'
        robot.slacker.chat.post_message(channel=channel, attachments=[attachments_dict], username=BOT_NAME,
                                        icon_url=ZABGRESS_ICON_URL)
        return

    if not robot.chrome.check_lock():
        lock_id = uuid4()
        if not (robot.chrome.lock(lock_id=lock_id)):
            attachments_dict['text'] = '`%s에 사용을 시작한 유저가 있습니다. 잠시만 기다려주세요`' % robot.chrome.locked_at
            robot.slacker.chat.post_message(channel=channel, attachments=[attachments_dict], username=BOT_NAME,
                                            icon_url=ZABGRESS_ICON_URL)
            return
    else:
        attachments_dict['text'] = '`%s에 사용을 시작한 유저가 있습니다. 잠시만 기다려주세요`' % robot.chrome.locked_at
        robot.slacker.chat.post_message(channel=channel, attachments=[attachments_dict], username=BOT_NAME,
                                        icon_url=ZABGRESS_ICON_URL)
        return

    # get response
    robot.logger.info('[%s] Getting Geolocation...' % (time.time() - start_time))
    keyword = ' '.join(tokens)
    data = get_location(keyword)
    if not len(data['results']):
        attachments_dict['text'] = '`구글에 주소 데이터가 없습니다.`'
        attachments_dict['color'] = RED
        robot.slacker.chat.post_message(channel=channel, attachments=[attachments_dict], username=BOT_NAME,
                                        icon_url=ZABGRESS_ICON_URL)
        robot.chrome.unlock()
        return

    # get address
    try:
        robot.logger.info('[%s] Finding Address...' % (time.time() - start_time))
        address = data['results'][0]['formatted_address']
        message = '%s\n' \
                  '`%s`' % (address, str(now))
    except Exception as e:
        robot.logger.info(e)
        robot.logger.info(data)
        attachments_dict['text'] = '`주소를 불러오는데 실패했습니다.`\n' \
                                   '>%s' % keyword
        attachments_dict['color'] = RED
        robot.slacker.chat.post_message(channel=channel, attachments=[attachments_dict], username=BOT_NAME,
                                        icon_url=ZABGRESS_ICON_URL)
        robot.chrome.unlock()
        return

    # parsing address
    try:
        robot.logger.info('[%s] Parsing Address...' % (time.time() - start_time))
        lat = round(float(data['results'][0]['geometry']['location']['lat']), 6)
        lng = round(float(data['results'][0]['geometry']['location']['lng']), 6)
        edge_west = data['results'][0]['geometry']['viewport']['southwest']['lng']
        edge_east = data['results'][0]['geometry']['viewport']['northeast']['lng']
        width = edge_east - edge_west

    except Exception as e:
        robot.logger.info(e)
        robot.logger.info(data)
        attachments_dict['text'] = '`좌표를 불러오는데 실패했습니다.`\n' \
                                   '>%s' % address
        attachments_dict['color'] = RED
        robot.slacker.chat.post_message(channel=channel, attachments=[attachments_dict], username=BOT_NAME,
                                        icon_url=ZABGRESS_ICON_URL)
        robot.chrome.unlock()
        return

    # Settings Zoom Level
    robot.logger.info('[%s] Setting Zoom Level...' % (time.time() - start_time))
    all_portal_zoom = 0.08
    if width < all_portal_zoom:
        z = 15
    else:
        z = 13
        extra_z = 0
        while width > all_portal_zoom * (2 ** (2 + extra_z)):
            extra_z += 1
        z -= extra_z

    # Notify Giphy
    robot.logger.info('[%s] Notify Giphy...' % (time.time() - start_time))
    try:
        attachments_dict['text'] = '`준비가 되는 동안 귀여운 거 보시죠`'
        attachments_dict['fallback'] = '준비가 되는 동안 귀여운 거 보시죠'
        giphy_queryset = ['puppy', 'dog', 'cat', 'kitten', 'rabbit', 'kangaroo']
        attachments_dict['image_url'] = get_giphy_image_url(choice(giphy_queryset))
    except Exception as e:
        robot.logger.info(e)
        attachments_dict['text'] = '귀여운걸 불러오는데 실패했어요... ㅠㅠ'
        attachments_dict['color'] = '귀여운걸 불러오는데 실패했어요... ㅠㅠ'
        giant_penguin_image_url = 'http://woman.chosun.com/editor/cheditor_new/attach/2019/AFW9NUB869E9LSXPF1Z4_1.jpg'
        attachments_dict['image_url'] = get_giphy_image_url(giant_penguin_image_url)
    finally:
        robot.slacker.chat.post_message(channel=channel, username='giphy', attachments=[attachments_dict],
                                        icon_url=GIPHY_ICON_URL)
        attachments_dict['image_url'] = None

    # Getting Intel Map
    robot.logger.info('[%s] Getting Intel Map...' % (time.time() - start_time))
    url = 'https://intel.ingress.com/intel?ll=%s,%s&z=%s' % (lat, lng, z)
    robot.logger.info(url)
    robot.chrome.driver.get(url)
    time.sleep(1)

    robot.logger.info('[%s] %s (lat: %s, lng: %s, z: %s)' % ((time.time() - start_time), keyword, lat, lng, z))
    if robot.chrome.driver.title != 'Ingress Intel Map':
        attachments_dict['text'] = '지도를 불러오는 데 실패했어요 ㅠㅠ'
        attachments_dict = dict()
        robot.slacker.chat.post_message(channel=channel, username='giphy', attachments=[attachments_dict],
                                        icon_url=GIPHY_ICON_URL)
        robot.chrome.unlock()
        return
    while True:
        current_time = int(time.time())
        spent_time = current_time - start_time
        robot.logger.info(spent_time)

        # Timeout
        if spent_time > MAX_LOAD_TIME:
            attachments_dict['text'] = '너무 오래걸리는 지역이라서 이정도만 보여드릴게요!\n' \
                                       '%s' % message
            attachments_dict['color'] = ORANGE
            break

        # Get Loading Percent
        try:
            loading_msg = robot.chrome.driver.find_element_by_id('loading_msg')
        except Exception as e:
            robot.logger.info(e)
            robot.logger.info(robot.chrome.driver.page_source)
            attachments_dict['text'] = '지도를 불러오긴 했는데... 로딩하는 도중에 실패했어요 ㅠㅠ'
            robot.slacker.chat.post_message(channel=channel, username=BOT_NAME, attachments=[attachments_dict],
                                            icon_url=ZABGRESS_ICON_URL)
            robot.chrome.unlock()
            return

        # Load Complete
        if loading_msg.get_attribute("style") == 'display: none;':
            attachments_dict['color'] = GREEN
            break
        time.sleep(1)

    # Saving Screenshot
    robot.logger.info('[%s] Saving Screenshot...' % (time.time() - start_time))
    filename = now.strftime('%Y%m%d%H%M%S')
    try:
        file_url = robot.chrome.save_screenshot(filename)
        attachments_dict['image_url'] = file_url
        attachments_dict['fallback'] = keyword
        attachments_dict['text'] = message
        attachments_dict['actions'] = [
            {
                "type": "button",
                "text": "크게보기",
                "url": file_url,
            }
        ]
    except Exception as e:
        message = '스크린샷 저장에 실패했어요... ㅠㅠ'
        attachments_dict['text'] = '`%s`' % message
        attachments_dict['color'] = RED
        attachments_dict['fallback'] = message
        robot.logger.info(e)

    robot.chrome.unlock()
    robot.slacker.chat.post_message(channel=channel, username=BOT_NAME, attachments=[attachments_dict],
                                    icon_url=ZABGRESS_ICON_URL)
