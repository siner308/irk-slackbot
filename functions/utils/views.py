import os
import datetime
import time
import re
import datetime
from PIL import Image
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from django.shortcuts import redirect
from intelbot.settings.base import get_secret
from selenium import webdriver
from portal.models import Cookie
from screenshot.models import Screenshot


@api_view()
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def get_cookie(request):
    email = get_secret("GOOGLE_ACCOUNT", "EMAIL")
    password = get_secret("GOOGLE_ACCOUNT", "PASSWORD")
    url = 'https://accounts.google.com/ServiceLogin/signinchooser?service=ah&passive=true&continue=https%3A%2F%2Fappengine.google.com%2F_ah%2Fconflogin%3Fcontinue%3Dhttps%3A%2F%2Fintel.ingress.com%2Fintel&flowName=GlifWebSignIn&flowEntry=ServiceLogin'
    # url = 'https://www.google.com/accounts/ServiceLogin?service=ah&passive=true&continue=https://appengine.google.com/_ah/conflogin%3Fcontinue%3Dhttps://www.ingress.com/intel&ltmpl='
    
    # selenium
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("disable-gpu")
    driver = webdriver.Chrome("api/chromedriver", chrome_options=chrome_options)

    # access to login
    print('access to login')
    driver.get(url)
    driver.find_element_by_name('Email').send_keys(email)
    driver.find_element_by_name('signIn').click()
    driver.find_element_by_name('Passwd').send_keys(password)
    driver.find_element_by_name('signIn').click()
    url = 'https://www.ingress.com/intel?ll=37.300554,127.229958&z=17'

    cookie = Cookie.objects.get(pk=1)

    driver.get(url)
    items = driver.get_cookies()
    source = driver.page_source.encode('utf-8').decode('utf-8')
    regex = r'src="/jsc/gen_dashboard_(\S+).js"'
    v = re.findall(regex, source)

    for item in items:
        if item['name'] == 'SACSID':
            sacsid = item['value']
            cookie.sacsid = sacsid
            print('sacsisd = %s' % sacsid)
        if item['name'] == 'csrftoken':
            csrftoken = item['value']
            cookie.csrftoken = csrftoken
            print('csrftoken = %s' % csrftoken)

    cookie.save()

    data = {
        'data': items,
        'v': v[0]
    }
    return Response(data=data)


def make_screenshot(request):
    # 구글 계정 정보
    print('get account info')
    email = get_secret("GOOGLE_ACCOUNT", "EMAIL")
    password = get_secret("GOOGLE_ACCOUNT", "PASSWORD")

    # 구글 로그인 url
    url = 'https://accounts.google.com/ServiceLogin/signinchooser?service=ah&passive=true&continue=https%3A%2F%2Fappengine.google.com%2F_ah%2Fconflogin%3Fcontinue%3Dhttps%3A%2F%2Fintel.ingress.com%2Fintel&flowName=GlifWebSignIn&flowEntry=ServiceLogin'

    # selenium
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("disable-gpu")

    driver = webdriver.Chrome("api/chromedriver", chrome_options=chrome_options)

    # access to login
    print('access to login')
    driver.get(url)

    driver.find_element_by_name('Email').send_keys(email)
    driver.find_element_by_name('signIn').click()
    driver.find_element_by_name('Passwd').send_keys(password)
    driver.find_element_by_name('signIn').click()

    file_path = 'kakao/static/img/anomaly/'
    # kakao image size : 720 x 630 px
    origin_bounding_box = (0, 150, 1920, 880)
    crop_bounding_box = (600, 150, 1330, 780)

    while(True):
        url = 'https://www.ingress.com/intel?ll=37.300554,127.229958&z=17'
        driver.get(url)
        cookie = Cookie.objects.get(pk=1)
        items = driver.get_cookies()

        # get SACSID, csrftoken
        for item in items:
            if item['name'] == 'SACSID':
                sacsid = item['value']
                cookie.sacsid = sacsid
                print('SACSID = %s' % sacsid)
            if item['name'] == 'csrftoken':
                csrftoken = item['value']
                cookie.csrftoken = csrftoken
                print('csrftoken = %s' % csrftoken)

        # get v
        source = driver.page_source.encode('utf-8').decode('utf-8')
        print(source)
        regex = r'src="/jsc/gen_dashboard_(\S+).js"'
        try:
            v = re.findall(regex, source)[0]
            cookie.v = v
            print('v = %s' % v)
        except:
            pass

        cookie.save()

        place = Screenshot.objects.filter(is_active=True).order_by('updated').first()
        print(place.place_name + ': ' + place.sha1 + ' (%s)' % datetime.datetime.now())

        file_name = place.sha1
        filename = file_path + file_name
        url = 'https://www.ingress.com/intel?ll=%f,%f&z=%d' % (place.lat, place.lag, place.zoom_level)

        driver.get(url)

        if place.place_name.startswith('링크'):
            print('sleep link')
            time.sleep(180)
        else:
            print('sleep portal')
            time.sleep(60)

        place.save()
            
        year = place.updated.year
        month = place.updated.month
        day = place.updated.day
        hour = place.updated.hour
        minute = place.updated.minute
        second = place.updated.second

        #os.system('rm ./%s*.png' % filename)
        filename = filename + '_%s%s%s%s%s%s' % (year, month, day, hour, minute, second)

        driver.save_screenshot(filename + '_hdd.png')
        base_image = Image.open(filename + '_hdd.png')
        cropped_image = base_image.crop(crop_bounding_box)
        cropped_image.save(filename + '_cropped.png')
        origin_image = base_image.crop(origin_bounding_box)
        origin_image.save(filename + '_origin.png')
