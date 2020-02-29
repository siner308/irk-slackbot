from selenium import webdriver

from functions.utils.google.auth import sign_in_google_from_intel_map
from logger import log_or_print
from settings import CHROMEDRIVER_PATH
from datetime import datetime


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

    def __init__(self):
        log_or_print('Initialize ChromeDriver Start...')
        self.driver = setup_chrome()
        self.get_intel_map()
        log_or_print('Initialize ChromeDriver Complete...')

    def lock(self, lock_id):
        if not self.check_lock():
            self.lock_id = lock_id
            self.locked_at = datetime.now().strftime('%yy-%mm-%dd %HH:MM:SS')
            return True
        return False

    def unlock(self):
        self.lock_id = None
        self.locked_at = None

    def check_lock(self):
        return self.lock_id

    def get_intel_map(self):
        self.driver = sign_in_google_from_intel_map(self.driver)

