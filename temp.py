import time
import typing

import requests
from requests import Timeout, TooManyRedirects
from config import *


base_url = "https://fapi.binance.com"
ticker_extension = "/fapi/v1/ticker/24hr"
kline_extension = "/fapi/v1/klines"

current_prices = []


def make_get_request(endpoint, data: typing.Dict):
    headers = {"X-MBX-APIKEY": BINANCE_FIRST_API}
    try:
        response = requests.get(endpoint, headers=headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error in calling {endpoint} endpoint, status code {response.status_code}, message {response.json()}")
            return None
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return None


def get_ticker_24h(symbol: str):
    """
    24 hour rolling window price change statistics. Careful when accessing this with no symbol.
    :param symbol: symbol name
    :return:
    """
    data = dict()
    data[symbol] = symbol
    ticker = make_get_request(base_url + ticker_extension, data)
    if ticker is not None:
        return ticker
    else:
        return None



def get_candlesticks(symbol: str, interval: str, limit: int):
    """
    Kline/candlestick bars for a symbol.
    Klines are uniquely identified by their open time.
    :param symbol: symbol name
    :param interval: interval = 1m,3m,5m,15m,30m,1h,2h,4h,6h,8h,12h,1d,3d,1w,1M
    :param limit: default 500; max 1000
    :return: array of arrays [Open time, Open, High, Low, Close, Volume,Close time,Quote asset volume,Number of trades,
                                Taker buy base asset volume,Taker buy quote asset volume,Ignore]
    """
    data = dict()
    data["interval"] = interval
    data["symbol"] = symbol
    data["limit"] = limit
    candlesticks = make_get_request(base_url + kline_extension, data)
    # print(*candlesticks, sep="\n")

    return candlesticks


def get_open_prices(candlesticks):
    open_prices = []
    for candle in candlesticks:
        open_prices.append(float(candle[1]))
    return open_prices



def get_current_price(symbol_obj: typing.List) -> float:
    seconds = 0
    while True:
        current_price = float(symbol_obj[0]["lastPrice"])
        if seconds % 60 == 0:
            current_prices.append(current_price)
        time.sleep(5)
        seconds += 5


def get_exchange_info(symbols=None):

    """
    Current exchange trading rules and symbol information
    :param symbols: none, one or more symbols in array
    :return: array of symbols info
    """

    if symbols is not None:
        data = dict()
        if len(symbols) == 1:
            data["symbol"] = symbols[0]
        elif len(symbols) > 1:
            data["symbols"] = symbols
        exchange_info = make_get_request(base_url + "/exchangeInfo?", data)
    else:
        exchange_info = make_get_request(base_url + "/exchangeInfo")
    return exchange_info



def _calculate_core(number):
    if 0 < number < 0.5:
        score = 1
    elif 0.5 <= number < 1:
        score = 1.25
    return score


prices = get_open_prices(get_candlesticks("BTCUSDT", "1m", 1000))


def calculate_score():
    try:
        change_2m = round(current_prices[-1] * 100 / prices[-2] - 100, 2)
        change_6h = round(current_prices[-1] * 100 / prices[-360] - 100, 2)
        average_30m = sum(prices[-30:]) / 30
        moving_average_30m = round(current_prices[-1] * 100 / average_30m - 100, 2)
        score = 0
        score += _calculate_core(change_2m)
        score += _calculate_core(change_6h)
        score += _calculate_core(moving_average_30m)
        return score

    except Exception as e:
        print(e)


