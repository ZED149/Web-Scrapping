import sqlite3
import datetime

import requests
from bs4 import BeautifulSoup

### YAHOO FINANCE SCRAPING
# this is the copy website url not the real one
MOST_ACTIVE_STOCKS_URL = "https://cs1951a-s21-brown.github.io/resources/stocks_scraping_2021.html"

### STONKS API ###
STONKS_API_URL = "http://localhost:8000"

# TODO: Part 1: Use BeautifulSoup and requests to collect data required for the assignment.
# importing libraries
import requests
from bs4 import BeautifulSoup

# making a request on the url
response = requests.get(MOST_ACTIVE_STOCKS_URL)
# checking if response is valid then process, else exit with a code 0
soup = BeautifulSoup(response.content, 'html5lib')
# table containing our data
table = soup.find('table', attrs={'class': 'genTbl closedTbl elpTbl elp25 crossRatesTbl'})

# TODO: Save data below.
# variable to hold scrapped information
quotes = {
    'Company Name': [],
    'Stock Symbol': [],
    "Price": [],
    "Change Percentage": [],
    'Volume': [],
    'HQ State': []
}

# scrapping company names
for row in table.findAll('td', attrs={'class': 'left bold plusIconTd elp'}):
    # print(row)
    quotes['Company Name'].append(row.a['title'])

# scrapping stock symbols and hq state as they both have none class associated with them
temp = []
for row in table.findAll('td', attrs={'class': None}):
    temp.append(row.text)

# assigning Stock Symbols
quotes['Stock Symbol'] = temp[0::2]
# removing spaces from stock symbols
quotes['Stock Symbol'] = [i.replace(" ", '') for i in quotes['Stock Symbol']]
# assigning HQ States
quotes['HQ State'] = temp[1::2]
# lower casing the HQ States
quotes['HQ State'] = [i.lower() for i in quotes['HQ State']]
# removing spaces from HQ States
quotes['HQ State'] = [i.replace(" ", "") for i in quotes['HQ State']]

# scrapping prices
for row in table.findAll('td', attrs={'class': 'align_right'}):
    quotes['Price'].append(row.text)

# converting prices from string to floats
quotes['Price'] = [i.replace(",", "") for i in quotes['Price']]
quotes['Price'] = [float(i) for i in quotes['Price']]

# scrapping Change Percentage
for row in table.findAll('td', attrs={'class': 'bold'}):
    quotes['Change Percentage'].append(row.text)

# rearranging our list
quotes['Change Percentage'] = quotes['Change Percentage'][2::3]
# converting change percentage from string to float
quotes['Change Percentage'] = [i.replace("%", '') for i in quotes['Change Percentage']]
quotes['Change Percentage'] = [float(i) for i in quotes['Change Percentage']]

# scrapping Volumes
for row in table.findAll('td'):
    quotes['Volume'].append(row.text)

quotes['Volume'] = quotes['Volume'][6::8]
# we need to filter volumes on the basis of
# K -> 1000
# M -> 1000000
# B -> 100000000
temp = []
for i in quotes['Volume']:
    if 'K' in i:
        value = i.replace('K', "")
        value = float(value)
        value = value * 1000
        temp.append(value)
    elif 'M' in i:
        value = i.replace('M', "")
        value = float(value)
        value = value * 1000000
        temp.append(value)
    elif 'B' in i:
        value = i.replace('B', "")
        value = float(value)
        value = value * 100000000
        temp.append(value)
# reassigning volume list
quotes['Volume'] = temp

# TODO: Part 2: Use Stonks API to collect historical trading data for your stocks.

average_closing_price_date = []     # date is January 20, 2023
for STOCK_SYMBOL in quotes['Stock Symbol']:
    url_for_avg_closing_price_date = f"http://127.0.0.1:8000/{STOCK_SYMBOL}/chart/date/2023-01-20"
    response = requests.get(url_for_avg_closing_price_date)
    average_closing_price_date.append(response.json()['close'])

# now calculating average closing price for each stock over the last month
month_back = (datetime.datetime.now() - datetime.timedelta(days=30))
closing_prices_sum = 0.0
avg_list = []
# iterating for each stock
for STOCK_SYMBOL in quotes['Stock Symbol']:
    closing_prices_sum = 0.00
    # for a whole month
    # assuming there are 30 days in a month
    for i in range(0, 30):
        # constructing url
        url = f"http://127.0.0.1:8000/{STOCK_SYMBOL}/chart/date/{month_back.strftime("%Y-%m-%d")}"
        # making request
        response = requests.get(url)
        # extracting close value
        closing_prices_sum = closing_prices_sum + float(response.json()['close'])
        # adding one day
        month_back = month_back + datetime.timedelta(days=1)

    # calculating avg and appending it to the list
    avg_list.append(int(closing_prices_sum / 30))

# Create connection to database

# Make sure if are unable to connect make sure you have the right path to data.db, this might cause
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Delete tables if they exist
c.execute('DROP TABLE IF EXISTS "companies";')
c.execute('DROP TABLE IF EXISTS "quotes";')

# TODO: Part 4: Create tables in the database and add data to it. REMEMBER TO COMMIT

# creating Companies table in DB
c.execute("""
CREATE TABLE "companies" (
	"symbol"	TEXT,
	"name"	TEXT,
	"location"	TEXT,
	PRIMARY KEY("symbol")
)
""")

# creating Quotes table in DB
c.execute("""
CREATE TABLE "quotes" (
	"symbol"	TEXT,
	"close"	INTEGER,
	"price"	INTEGER,
	"avg_price"	INTEGER,
	"volume"	INTEGER,
	"change_pct"	REAL,
	FOREIGN KEY("symbol") REFERENCES "companies"("symbol"),
	PRIMARY KEY("symbol")
);
""")

# now that we have created our tables
# we need to store data into it

# inserting into companies table
for symbol, name, location in zip(quotes['Stock Symbol'], quotes['Company Name'], quotes['HQ State']):
    query = """
        INSERT INTO companies (symbol,name,location) VALUES (?,?,?)
        """
    c.execute(query, (symbol, name, location))
    conn.commit()

# inserting into quotes table
for symbol, close, price, avg_price, volume, change_pct in zip(quotes['Stock Symbol'],
                                                               average_closing_price_date, quotes['Price'],
                                                               avg_list, quotes['Volume'], quotes['Change Percentage']):
    query = """
        INSERT INTO quotes (symbol,close,price,avg_price,volume,change_pct) VALUES (?,?,?,?,?,?)
        """
    c.execute(query, (symbol, close, price, avg_price, volume, change_pct))
    conn.commit()

# committing changes
conn.commit()
# closing connection to DB
conn.close()



