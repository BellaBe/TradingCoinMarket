import json
import time

import pandas as pd
import pyttsx3 as pyttsx3

from config import *
import requests
from requests import Timeout, TooManyRedirects
import pyttsx3

df = pd.read_csv("coins.csv", usecols=["Symbol", "Up", "Down"])
print(df)

df = df.to_json()
df = json.loads(df)

symbols = df["Symbol"]
ups = df["Up"]
downs = df["Down"]

symbols = [symbols[x] for x in symbols]
ups = [1000000 if ups[x] is None else float(ups[x]) for x in ups]
downs = [0 if downs[x] is None else float(downs[x]) for x in downs]


current_prices = []

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

parameters = {
    'start': '1',
    'limit': '5000',
    'convert': 'GBP'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': COIN_MARKET_API,
}

engine = pyttsx3.init()


def printing():
    while True:
        try:
            response = requests.get(url, params=parameters, headers=headers)
            data = response.json()["data"]
            for d in data:
                if d["name"] in symbols:
                    current_prices.append(float(d["quote"]["GBP"]["price"]))
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
        print(current_prices)
        for index in range(len(symbols)):
            if current_prices[index] > ups[index]:
                speak(f"Price for {symbols[index]} reached upper limit and it is {current_prices[index]}")
            elif current_prices[index] < downs[index]:
                speak(f"Price for {symbols[index]} reached down limit and it is {current_prices[index]}")
        current_prices.clear()

        time.sleep(300)


def speak(msg):
    print(msg)
    engine.say(msg)
    engine.runAndWait()


printing()
