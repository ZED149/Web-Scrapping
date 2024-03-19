
import requests

url = "https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=345427200&period2=1710720000&interval=1d&events=history&includeAdjustedClose=true"

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}

response = requests.get(url, headers=headers)

# writing to a file
with open("AAPL.csv", "wb") as f:
    f.write(response.content)

