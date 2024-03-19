from selenium import webdriver
from selenium.webdriver.chrome.service import Service
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
    driver.get("http://automated.pythonanywhere.com")
    return driver


# main

driver = get_driver()
time.sleep(2)
element = driver.find_element(by="xpath", value='/html/body/div[1]/div/h1[2]')
quote = driver.find_element(by="xpath", value='/html/body/div[1]/div/h1[1]')
# extracting only number
temperature = float(element.text.split(": ")[1])
print(temperature)
print(quote.text)
