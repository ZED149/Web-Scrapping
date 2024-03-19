

import requests
from bs4 import BeautifulSoup

url = "https://www.x-rates.com/calculator/?from=USD&to=PKR&amount=120"
# making request
response = requests.get(url)

# creating soup
soup = BeautifulSoup(response.text, "html.parser")
# extracting rates
rates = soup.find(class_="ccOutputRslt")
# printing rates
print(rates.text)
