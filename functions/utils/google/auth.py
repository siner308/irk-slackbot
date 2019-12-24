import time
from bs4 import BeautifulSoup


def signin_google(driver, email, password):
    url = 'https://intel.ingress.com'
    google_sign_in_url = None
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    a_tags = soup.find_all('a')
    for a_tag in a_tags:
        href = a_tag.get('href')
        if href.find('accounts.google.com') and href.find('intel.ingress.com'):
            google_sign_in_url = href
            print(google_sign_in_url)
            break

    if not google_sign_in_url:
        raise ValueError

    driver.get(google_sign_in_url)
    time.sleep(3)
    driver.find_element_by_name('Email').send_keys(email)
    driver.find_element_by_name('signIn').click()
    time.sleep(1)
    driver.find_element_by_name('Passwd').send_keys(password)
    driver.find_element_by_name('signIn').click()
    time.sleep(1)
    try:
        driver.find_element_by_id('submit_approve_access').click()
        time.sleep(3)
    except Exception as e:
        print(e)
        raise Exception
    return driver
