# python
from time import sleep

# library
from bs4 import BeautifulSoup

# local
from settings import GOOGLE_EMAIL, GOOGLE_PASSWORD, INGRESS_AGENT_NAME


def sign_in_google_from_intel_map(driver, robot):
    robot.logger.info('Signing In Google From Intel Map...')
    url = 'https://intel.ingress.com'
    google_sign_in_url = None
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    a_tags = soup.find_all('a')
    for a_tag in a_tags:
        href = a_tag.get('href')
        if href.find('accounts.google.com') and href.find('intel.ingress.com'):
            google_sign_in_url = href
            robot.logger.info(google_sign_in_url)
            break

    if not google_sign_in_url:
        raise ValueError

    driver.get(google_sign_in_url)
    sleep(1)
    driver.find_element_by_name('Email').send_keys(GOOGLE_EMAIL)
    driver.find_element_by_name('signIn').click()
    sleep(1)
    driver.find_element_by_name('Passwd').send_keys(GOOGLE_PASSWORD)
    driver.find_element_by_id('submit').click()
    sleep(1)
    driver.find_element_by_id('submit_approve_access').click()
    sleep(1)

    # Check Success
    robot.logger.info('Finding Agent Name from Page Source...')
    while driver.page_source.find(INGRESS_AGENT_NAME) == -1:
        sleep(1)
    robot.logger.info('Sign In Google Complete!!!')
    sleep(1)
    robot.logger.info(driver.page_source)
    return driver
