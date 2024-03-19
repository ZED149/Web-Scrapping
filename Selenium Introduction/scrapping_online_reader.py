from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime

service = Service("C:\\Users\\salma\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")



def get_driver():
    # Set options to make browsing easier
    options = webdriver.ChromeOptions()
    options.add_argument('disable-infobars')
    options.add_argument('start-maximized')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('no-sandbox')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("disbale-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=service, options=options)
    url = "https://titan22.com/account/login?return_url=%2Faccount"
    driver.get(url)
    return driver


# main
# initializing driver
driver = get_driver()
# entering username
driver.find_element(by="id", value="CustomerEmail").send_keys("app7flask@gmail.com")
time.sleep(2)
# entering password
driver.find_element(by="id", value="CustomerPassword").send_keys("??!65EhGMg8.WwY" + Keys.RETURN)
time.sleep(2)
# clicking on Contact Us
driver.find_element(by="xpath", value="/html/body/footer/div/section/div/div[1]/div[1]/div[1]/nav/ul/li[1]/a").click()
time.sleep(2)
