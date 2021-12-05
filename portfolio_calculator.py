from config import *
import requests
from prettytable import PrettyTable

from requests import ConnectionError, Timeout, TooManyRedirects

file = open("portfolio.txt", "r")
coins = []
quantities = []
buying_prices = []
buy_value = 0
current_value = 0


def color(item):
    if item > 0:
        return "\033[92m" + str(item) + "\033[0m"
    else:
        return "\033[91m" + str(item) + "\033[0m"


for line in file.readlines()[1:]:
    line = line.split(",")
    coins.append(line[0])
    quantities.append(float(line[1]))
    buying_prices.append(float(line[2]))

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

table = PrettyTable()
table.field_names = ["NAME", "SYMBOL", "QUANTITY", "CURRENT PRICE", "BUY PRICE", "PROFIT %", "CHANGE 1h", "CHANGE 24h", "CHANGE 7d"]

try:
    response = requests.get(url, params=parameters, headers=headers)
    data = response.json()["data"]
    # print(*data, sep="\n")
    for d in data:
        if d["name"] in coins:
            index = coins.index(d["name"])
            current_price = float(d["quote"]["GBP"]["price"])
            change_1h = float(d["quote"]["GBP"]["percent_change_1h"])
            change_24h = float(d["quote"]["GBP"]["percent_change_24h"])
            change_7d = float(d["quote"]["GBP"]["percent_change_7d"])
            profit = round(current_price / buying_prices[index] * 100 - 100, 2)
            buy_value += buying_prices[index] * quantities[index]
            current_value += current_price * quantities[index]
            row = [d["name"], d["symbol"], quantities[index], current_price, buying_prices[index], color(profit), color(change_1h), color(change_24h), color(change_7d)]
            table.add_row(row)


except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

print(table)

total_profit = current_value / buy_value * 100 - 100
total_profit_in_fiat = current_value - buy_value

print(f"Portfolio value: {current_value}, total profit {round(total_profit, 2)}%, total profit in GBP {total_profit_in_fiat}")
