import os
from time import sleep
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image

from settings import GOOGLE_EMAIL, GOOGLE_PASSWORD, INGRESS_AGENT_NAME
from settings import CHROMEDRIVER_PATH, STATIC_ROOT, SERVER_URL


def setup_chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome("%s" % CHROMEDRIVER_PATH, chrome_options=chrome_options)
    return driver


class ChromeDriver:
    driver = None
    lock_id = None
    locked_at = None
    origin_bounding_box = (20, 140, 1860, 880)

    def __init__(self, robot):
        robot.logger.info('Initialize ChromeDriver Start...')
        self.driver = setup_chrome()
        self.driver = self.sign_in_google_from_intel_map(robot)
        robot.logger.info('Initialize ChromeDriver Complete...')

    def lock(self, lock_id):
        if not self.check_lock():
            self.lock_id = lock_id
            self.locked_at = datetime.now().strftime('%H:%M:%S')
            return True
        return False

    def unlock(self):
        self.lock_id = None
        self.locked_at = None

    def check_lock(self):
        return self.lock_id

    def save_screenshot(self, filename):
        file_dir = STATIC_ROOT + '/screenshots/'
        png_file_path = file_dir + filename + '.png'
        jpg_file_path = file_dir + filename + '.jpg'
        self.driver.save_screenshot(png_file_path)
        base_image = Image.open(png_file_path)
        cropped_image = base_image.crop(self.origin_bounding_box)
        rgb_im = cropped_image.convert('RGB')
        rgb_im.save(jpg_file_path)
        file_url = SERVER_URL + '/screenshots/' + filename + '.jpg'
        try:
            os.remove(png_file_path)
        except Exception as e:
            print(e)
            pass
        return file_url

    def sign_in_google_from_intel_map(self, robot):
        robot.logger.info('Signing In Google From Intel Map...')
        url = 'https://intel.ingress.com'
        google_sign_in_url = None
        self.driver.get(url)

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        a_tags = soup.find_all('a')
        for a_tag in a_tags:
            href = a_tag.get('href')
            if href.find('accounts.google.com') and href.find('intel.ingress.com'):
                google_sign_in_url = href
                robot.logger.info(google_sign_in_url)
                break

        if not google_sign_in_url:
            raise ValueError

        self.driver.delete_all_cookies()
        self.driver.get(google_sign_in_url)
        sleep(1)
        self.driver.find_element_by_name('Email').send_keys(GOOGLE_EMAIL)
        self.driver.find_element_by_name('signIn').click()
        sleep(1)
        self.driver.find_element_by_name('Passwd').send_keys(GOOGLE_PASSWORD)
        self.driver.find_element_by_id('signIn').click()
        sleep(1)
        self.driver.find_element_by_id('submit_approve_access').click()
        sleep(1)
        # Check Success
        cnt = 0
        robot.logger.info('Finding Agent Name from Page Source...')
        while self.driver.page_source.find(INGRESS_AGENT_NAME) == -1:
            sleep(1)
            robot.logger.info('Try Again...')
            cnt += 1
            if cnt > 10:
                print(self.driver.page_source)
                raise PermissionError
        robot.logger.info('Sign In Google Complete!!!')
        sleep(1)
        return self.driver
