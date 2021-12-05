import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from config import *
from prettytable import PrettyTable
import csv
import os
from openpyxl import Workbook

column_names = ["INDEX", "NAME", "SYMBOL", "PRICE", "VOLUME 24h", "% CHANGE 1h", "% CHANGE 24h",
                "% CHANGE 7d", "% CHANGE 30d", "% CHANGE 60d", "% CHANGE 90d", "MARKET CAPITALISATION"]

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

# Create table to append
table = PrettyTable()
table.field_names = column_names

# Create File to append
file = Workbook()
sheet = file.create_sheet("CoinMarketData")
sheet.append(column_names)


def is_none(number):
    if number:
        return float(number)
    return 0


coins = []
i = 1

try:
    response = requests.get(url, params=parameters, headers=headers)
    data = response.json()["data"]
    # print(*data, sep="\n")
    for d in data:
        index = i
        name = d["name"]
        symbol = d["symbol"]
        price = d["quote"]["GBP"]["price"]
        volume_24 = d["quote"]["GBP"]["volume_24h"]
        percent_change_1h = d["quote"]["GBP"]["percent_change_1h"]
        percent_change_24h = d["quote"]["GBP"]["percent_change_24h"]
        percent_change_7d = d["quote"]["GBP"]["percent_change_7d"]
        percent_change_30d = d["quote"]["GBP"]["percent_change_30d"]
        percent_change_60d = d["quote"]["GBP"]["percent_change_60d"]
        percent_change_90d = d["quote"]["GBP"]["percent_change_90d"]
        market_cap = d["quote"]["GBP"]["market_cap"]

        # table.add_row([name, symbol, exchange_currency, is_none(price), is_none(volume_24), is_none(percent_change_1h), is_none(percent_change_24h),
        #                is_none(percent_change_7d), is_none(percent_change_30d), is_none(percent_change_60d), is_none(percent_change_90d), is_none(market_cap)])

        line = [index, name, symbol, is_none(price), is_none(volume_24), is_none(percent_change_1h),
                is_none(percent_change_24h),
                is_none(percent_change_7d), is_none(percent_change_30d), is_none(percent_change_60d),
                is_none(percent_change_90d), is_none(market_cap)]

        coins.append(line)
        sheet.append(line)

        i += 1

except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

# print(table[:100])

file.save("coin_market_data.xlsx")


# while True:
#     print("Press: ")
#     number = 1
#     for item in table.field_names:
#         print(f"{str(number)}. Sort buy {item}")
#         number += 1
#     choice = input("Choose sort option: ")
#
#     print(f"************* Sorted by {table.field_names[int(choice) - 1]}")
#     print("Price in GBP")
#
#     coins.sort(key=lambda x: x[int(choice) - 1])
#     coins.reverse()
#     [table.add_row(coin) for coin in coins[:100]]
#     os.system("cls")
#     print(table)
#     table.clear_rows()

# file = open("data.csv", "a+", newline="", encoding="utf-8")
#     lines = []
#     line = [
#         name,
#         symbol,
#         slug,
#         market_pairs,
#         date_added,
#         tags,
#         max_supply,
#         circulating_supply,
#         total_supply,
#         #platform,
#         cmc_rank,
#         last_updated,
#         exchange_currency,
#         price,
#         volume_24,
#         percent_change_1h,
#         percent_change_24h,
#         percent_change_7d,
#         percent_change_30d,
#         percent_change_60d,
#         percent_change_90d,
#         market_cap
#     ]
#     lines.append(line)
# with file:
#     write = csv.writer(file)
#     write.writerows(lines)

######
# slug,
# market_pairs,
# date_added,
# tags,
# max_supply,
# circulating_supply,
# total_supply,
# #platform,
# cmc_rank,
# last_updated,
######
# slug = d["slug"]
# market_pairs = d["num_market_pairs"]
# date_added = d["date_added"]
# tags = ",".join(d["tags"])
# max_supply = d["max_supply"]
# circulating_supply = d["circulating_supply"]
# total_supply = d["total_supply"]
# cmc_rank = d["cmc_rank"]
# last_updated = d["last_updated"]
######
# "SLUG",
# "NUM_MARKET_PAIRS",
# "DATE ADDED",
# "TAGS",
# "MAX SUPPLY",
# "CIRCULATION SUPPLY",
# "TOTAL SUPPLY",
# "PLATFORM",
# "CMC RANK",
# "LAST UPDATED",
