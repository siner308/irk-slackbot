import os
from selenium import webdriver
from settings import CHROMEDRIVER_PATH


def setup_chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-default-browser-check")
    # chrome_options.add_argument("--no-first-run")
    # chrome_options.add_extension('./projects/irk/irk-slackbot/4.8.41_0.crx')
    driver = webdriver.Chrome("%s" % CHROMEDRIVER_PATH, chrome_options=chrome_options)
    return driver
