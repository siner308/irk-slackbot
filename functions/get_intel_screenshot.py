# coding: utf-8
from __future__ import unicode_literals
import os
import datetime
import time
from random import choice

from PIL import Image
from functions.decorators import on_command
from gevent.monkey import patch_all
from slack import slack_notify
from settings import ZABGRESS_ICON_URL, GIPHY_ICON_URL, GOOGLE_EMAIL, GOOGLE_PASSWORD, \
    STATIC_ROOT, SERVER_URL, CHANNEL, RED, ORANGE, CHROMEDRIVER_PATH, \
    GREEN
from chromedriver import setup_chrome
from functions.utils.google.auth import signin_google
from functions.utils.google.maps import get_location
from functions.giphy import get_giphy_image_url
from logger import get_logger

logger = get_logger('irk')

patch_all()

@on_command(['인텔', 'intel'])
def run(robot=None, channel=None, user=None, tokens=None):
    start_time = int(time.time())
    driver = None
    if not channel:
        channel = CHANNEL

    BOT_NAME = 'intel'
    text = '`고장났으면 신나를 외쳐!`'
    is_success = True
    slack_message = None
    attachments_dict = dict()
    attachments_dict['fallback'] = BOT_NAME
    attachments_dict['mrkdwn_in'] = ['text']

    file_dir = STATIC_ROOT + '/screenshots/'
    origin_bounding_box = (20, 140, 1860, 880)
    now = datetime.datetime.now()

    tokens = list(tokens)

    # send help information
    if not len(tokens):
        text = '*!인텔 또는 !intel* 명령어 입력 후, 원하는 위치의 주소를 아는대로 적어주시면 됩니다.\n' \
               'ex1) `!인텔 해운대 해수욕장` ex2) `!intel 올림픽공원`'
        is_success = False
    else:
        keyword = ' '.join(tokens)

    if is_success:
        try:
            driver = setup_chrome()
        except Exception as e:
            logger.error(e)
            is_success = False
            attachments_dict['color'] = RED

    if is_success:
        try:
            driver = signin_google(driver=driver, email=GOOGLE_EMAIL, password=GOOGLE_PASSWORD)
        except Exception as e:
            logger.error(e)
            is_success = False
            attachments_dict['color'] = RED

    if is_success:
        # get response
        data = get_location(keyword)
        if not len(data['results']):
            is_success = False
            text = '`구글에 주소 데이터가 없습니다.`'
            attachments_dict['color'] = RED

    # get address
    if is_success:
        try:
            address = data['results'][0]['formatted_address']
            text = '%s\n' \
                   '`%s`' % (address, str(now))
        except Exception as e:
            logger.error(e)
            logger.error(data)
            is_success = False
            text = '`주소를 불러오는데 실패했습니다.`\n' \
                   '>%s' % data
            attachments_dict['color'] = RED

    if is_success:
        try:
            lat = data['results'][0]['geometry']['location']['lat']
            lng = data['results'][0]['geometry']['location']['lng']
            edge_west = data['results'][0]['geometry']['viewport']['southwest']['lng']
            edge_east = data['results'][0]['geometry']['viewport']['northeast']['lng']
            width = edge_east - edge_west
        except Exception as e:
            logger.error(e)
            logger.error(data)
            is_success = False
            text = '`좌표를 불러오는데 실패했습니다.`'
            attachments_dict['color'] = RED

    if is_success:
        all_portal_zoom = 0.08
        if width < all_portal_zoom:
            z = 15
        else:
            z = 13
            extra_z = 0
            while width > all_portal_zoom * (2 ** (2 + extra_z)):
                extra_z += 1
            z -= extra_z

    if is_success:
        url = 'https://intel.ingress.com/intel?ll=%s,%s&z=%s' % (lat, lng, z)
        attachments_dict['text'] = '`준비가 되는 동안 귀여운 거 보시죠`'
        attachments_dict['fallback'] = '준비가 되는 동안 귀여운 거 보시죠'
        giphy_queryset = ['puppy', 'dog', 'cat', 'kitten', 'rabbit', 'kangaroo']
        attachments_dict['image_url'] = get_giphy_image_url(choice(giphy_queryset))
        attachments = [attachments_dict]
        slack_notify(text=slack_message, channel=channel, username='giphy', attachments=attachments,
                     icon_url=GIPHY_ICON_URL)
        try:
            driver.get(url)
            time.sleep(3)
            print(driver.current_url)
            if driver.title != 'Ingress Intel Map':
                print(driver.title)
                is_success = False
                text = '고장났어!'
                attachments_dict = dict()
            while True and is_success:
                current_time = int(time.time())
                spent_time = current_time - start_time
                if spent_time > 300:
                    text = '너무 오래걸리는 지역이라서 이정도만 보여드릴게요!\n' \
                           '%s' % text
                    attachments_dict['color'] = ORANGE
                    break
                try:
                    loading_msg = driver.find_element_by_xpath('//*[@id="loading_msg"]')
                except:
                    logger.error(driver.page_source)
                    is_success = False
                    text = '고장나면 신나!'
                    attachments_dict = dict()
                    break
                if loading_msg.get_attribute("style") == 'display: none;':
                    attachments_dict['color'] = GREEN
                    break
                time.sleep(1)

        except Exception as e:
            logger.error(e)
            is_success = False

    if is_success:
        filename = now.strftime('%Y%m%d%H%M%S')
        png_file_path = file_dir + filename + '.png'
        jpg_file_path = file_dir + filename + '.jpg'
        try:
            driver.save_screenshot(png_file_path)
            base_image = Image.open(png_file_path)
            cropped_image = base_image.crop(origin_bounding_box)
            rgb_im = cropped_image.convert('RGB')
            rgb_im.save(jpg_file_path)
            file_url = SERVER_URL + '/screenshots/' + filename + '.jpg'
            os.remove(png_file_path)
            attachments_dict['image_url'] = file_url
            attachments_dict['fallback'] = keyword
            attachments_dict['actions'] = [
                {
                    "type": "button",
                    "text": "크게보기",
                    "url": file_url,
                }
            ]
        except Exception as e:
            logger.error(e)

    if driver:
        if not is_success:
            # logger.error(driver.page_source)
            # logger.error(driver.title)
            # logger.error(driver.current_url)
            pass
        driver.quit()

    attachments_dict['text'] = text
    attachments = [attachments_dict]
    slack_notify(text=slack_message, channel=channel, username=BOT_NAME, attachments=attachments,
                 icon_url=ZABGRESS_ICON_URL)


response = {
    'results': [
        {
            'formatted_address': '508 Pungnap-dong, Songpa-gu, Seoul, South Korea',
            'geometry': {
                'location': {
                    'lng': 127.1128253,
                    'lat': 37.5294471
                },
                'location_type': 'ROOFTOP',
                'viewport': {
                    'southwest': {
                        'lng': 127.1114763197085,
                        'lat': 37.5280981197085
                    },
                    'northeast': {
                        'lng': 127.1141742802915,
                        'lat': 37.5307960802915
                    }
                }
            },
            'types': [
                'establishment',
                'point_of_interest'
            ],
            'plus_code': {
                'global_code': '8Q99G4H7+Q4',
                'compound_code': 'G4H7+Q4 Seoul, South Korea'},
            'place_id': 'ChIJM-1YD0OlfDURcy4Pk5T1iBA',
            'address_components': [
                {
                    'long_name': '508',
                    'short_name': '508',
                    'types': [
                        'premise'
                    ]
                },
                {
                    'long_name': 'Pungnap-dong',
                    'short_name': 'Pungnap-dong',
                    'types': [
                        'political',
                        'sublocality',
                        'sublocality_level_2'
                    ]
                },
                {
                    'long_name': 'Songpa-gu',
                    'short_name': 'Songpa-gu',
                    'types': [
                        'political',
                        'sublocality',
                        'sublocality_level_1'
                    ]
                },
                {
                    'long_name': 'Seoul',
                    'short_name': 'Seoul',
                    'types': [
                        'administrative_area_level_1',
                        'political'
                    ]
                },
                {
                    'long_name': 'South Korea',
                    'short_name': 'KR',
                    'types': [
                        'country',
                        'political'
                    ]
                },
                {
                    'long_name': '138-040',
                    'short_name': '138-040',
                    'types': [
                        'postal_code'
                    ]
                }
            ]
        }
    ],
    'status': 'OK'
}
