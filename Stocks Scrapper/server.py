"""
This is the source code of a mock API server providing fake stock data for the purpose of the webscraping assignment.
You are welcome to read through the content, but please do not change anything in here. The autograder has its own copy
of this file and will run that instead when grading your assignment, so changing anything in this file will cause you to
see something different than what would happen on the autograder.

To launch the server, open a separate terminal window, activate the course Python environment, ensure that you are `cd`'d
into the root of the stencil folder, and run:

```bash
uvicorn server:app
```

The server is available at `localhost:8000`. Documentation is available at `localhost:8000/docs`.

This should work just fine on the department machine, except the documentation is not accessible from a local web browser.
Therefore, a copy of the documentation is separately maintained at https://csci1951a-spring-2024.github.io/stonks-docs/.
Should the Stonks API change, the documentation must be manually updated at https://github.com/csci1951a-spring-2024/stonks-docs/, following the instructions there.
"""

import datetime
from dataclasses import dataclass

import numpy as np
import requests
from fastapi import FastAPI, HTTPException

resp = requests.get(
    'https://raw.githubusercontent.com/csci1951a-spring-2024/data/main/assignments/scraping/nasdaq_tickers.txt')
if not resp.ok:
    raise RuntimeError('Failed to download list of NASDAQ tickers')

VALID_TICKERS = set(resp.text.splitlines())


def generate_prices(n: int) -> np.ndarray:
    starting_price = np.random.rand() * 20 + 20  # [20, 40]
    deltas = np.random.randn(n) * 2
    return starting_price + np.cumsum(deltas)


def get_stock_prices_on_date(symbol: str, date: datetime.date) -> (np.ndarray, np.ndarray):
    np.random.seed(hash((
        symbol,
        date,
    )) % (2 ** 31))
    n_entries = np.random.randint(30, 60)
    prices = generate_prices(n_entries)
    volumes = np.random.randint(20000, 30000, size=n_entries)
    return prices, volumes


@dataclass
class Chart:
    symbol: str
    date: datetime.date
    open: float
    close: float
    low: float
    high: float
    volume: float


def to_float(n) -> float:
    return int(float(n) * 100) / 100


def output_chart(symbol, date, prices, volumes) -> Chart:
    return {
        "symbol": symbol,
        "date": date,
        "open": to_float(prices[0]),
        "close": to_float(prices[-1]),
        "low": to_float(np.min(prices)),
        "high": to_float(np.max(prices)),
        "volume": to_float(np.sum(volumes)),
    }


description = """
Stonks API allows you to query the trading prices of stock symbols on different days.
This is a mock API to simulate online APIs and only implements a subset of functionalities that real APIs would provide.
Therefore, it makes many simplifying assumptions about how stock markets work.
If you're interested in learning more, [this guide](https://www.nerdwallet.com/article/investing/how-to-interpret-stock-charts-and-data) gives a good overview of how to read a real stock chart.

Please note that the data displayed are mocked using random number generators for instructional purposes and are not actual market data.
"""

tags_metadata = [
    {
        "name": "Historical Data",
        "description": "Summaries of trading activity of a security to the granularity of a day.",
    },
]


app = FastAPI(
    title="Stonks",
    description=description,
    openapi_tags=tags_metadata,
)


def validate_symbol(symbol: str) -> str:
    symbol = symbol.upper()
    if symbol not in VALID_TICKERS:
        raise HTTPException(status_code=404, detail=f'{symbol} not found')
    return symbol


@app.get(
    "/{symbol}/chart/date/{date}",
    tags=["Historical Data"],
    summary="Get a single day's trading data",
    description="Return a summary of trading activity about a security on a given date. Symbol can be in any case. The date is specified in [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) format; e.g., 2008-09-15.",
    response_description="Summary of a single day's trading activity, including the prices of the security at market open and close, the lowest and highest prices of the security throughout the day, and the trading volume.",
    responses={
        404: {}
    }
)
def read_chart_date(symbol: str, date: datetime.date) -> Chart:
    symbol = validate_symbol(symbol)
    prices, volumes = get_stock_prices_on_date(symbol, date)
    return output_chart(symbol, date, prices, volumes)


@dataclass
class Charts:
    symbol: str
    start_date: datetime.date
    end_date: datetime.date
    charts: list[Chart]


def read_charts_on_date_range(symbol: str, start_date: datetime.date, end_date: datetime.date) -> (np.ndarray, np.ndarray):
    charts = []
    while start_date <= end_date:
        charts.append(read_chart_date(symbol, start_date))
        start_date = start_date + datetime.timedelta(days=1)
    return {
        "symbol": symbol,
        "start_date": start_date,
        "end_date": end_date,
        "charts": charts,
    }


@app.get(
    "/{symbol}/chart/1w",
    tags=["Historical Data"],
    summary="Get last week's trading data",
    description="Return the summaries of trading activity on each day over the last 7 calendar days about a security. Symbol can be in any case.",
    responses={
        404: {}
    }
)
def read_chart_1w(symbol: str) -> Charts:
    symbol = validate_symbol(symbol)
    today = datetime.date.today()
    return read_charts_on_date_range(symbol, today - datetime.timedelta(days=7), today)


@app.get(
    "/{symbol}/chart/1m",
    tags=["Historical Data"],
    summary="Get last month's trading data",
    description="Return the summaries of trading activity on each day over the last 30 calendar days about a given security. Symbol can be in any case.",
    responses={
        404: {}
    }
)
def read_chart_1m(symbol: str) -> Charts:
    symbol = validate_symbol(symbol)
    today = datetime.date.today()
    return read_charts_on_date_range(symbol, today - datetime.timedelta(days=30), today)


@app.get(
    "/{symbol}/chart/3m",
    tags=["Historical Data"],
    summary="Get last three month's trading data",
    description="Return the summaries of trading activity on each day over the last 90 calendar days about a given security. Symbol can be in any case.",
    responses={
        404: {}
    }
)
def read_chart_3m(symbol: str) -> Charts:
    symbol = validate_symbol(symbol)
    today = datetime.date.today()
    return read_charts_on_date_range(symbol, today - datetime.timedelta(days=90), today)
