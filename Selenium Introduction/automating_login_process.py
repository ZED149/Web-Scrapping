from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time

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
    url = "http://automated.pythonanywhere.com/login/"
    driver.get(url)
    return driver


# main

driver = get_driver()
driver.find_element(by="id", value="id_username").send_keys("automated")
driver.find_element(by="id", value="id_password").send_keys("automatedautomated" + Keys.RETURN)
driver.find_element(by="xpath", value="/html/body/nav/div/a").click()
time.sleep(2)
temperature = driver.find_element(by="xpath", value="/html/body/div[1]/div/h1[2]").text.split(": ")[1]
print(temperature)
