def signin_google(driver, email, password):
    url = 'https://accounts.google.com/ServiceLogin/signinchooser' \
          '?service=ah' \
          '&passive=true' \
          '&continue=https%3A%2F%2Fappengine.google.com%2F_ah%2Fconflogin%3Fcontinue%3Dhttps%3A%2F%2Fintel.ingress.com%2Fintel' \
          '&flowName=GlifWebSignIn' \
          '&flowEntry=ServiceLogin'
    driver.get(url)
    driver.find_element_by_name('Email').send_keys(email)
    driver.find_element_by_name('signIn').click()
    driver.find_element_by_name('Passwd').send_keys(password)
    driver.find_element_by_name('signIn').click()
    return driver