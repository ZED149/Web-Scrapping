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
    url = "https://automated.pythonanywhere.com/"
    driver.get(url)
    return driver


# main
# initializing driver
driver = get_driver()
# executing the script every 2 seconds
while True:
    time.sleep(2)
    # scrapping temperature
    temperature = driver.find_element(by="xpath", value="/html/body/div[1]/div/h1[2]").text.split(": ")[1]
    # writing it to a file
    filename = datetime.now().strftime("%Y-%m-%d.%H-%M-%S")
    with open(f"{filename}.txt", "w") as file:
        file.write(temperature + ",\n")
    # closing driver
