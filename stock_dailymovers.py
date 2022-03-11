import yfinance as yf
import pandas as pd
import time
import random

import stock_manager
import stock_voice

DAILYMOVERS_REQUEST_LIST = []
TOP_MOVERS = []

url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt"
df=pd.read_csv(url, sep="|")

def lookup_fn(df, key_row, key_col):
    try:
        return df.iloc[key_row][key_col]
    except IndexError:
        return 0

def load_phrases():
    with open("stock_dailymovers_request", "r") as f:
        for line in f:
            DAILYMOVERS_REQUEST_LIST.append(
                line.strip().replace("'", "").replace("[", "").replace("]", "").replace("-", ""))


def init_dailymovers_request():
    TOP_MOVERS = stock_manager.get_day_gainers()





init_dailymovers_request()
print(stock_manager.get_day_gainers().get(3))
#print(stock_manager.get_day_gainers())

def say_top_movers():
    random_num = random.randint(1, 2)

    stock_voice.speak("How many would you like me to list? Max is 10.")

    if random_num == 1:
        stock_voice.speak("Here are the top five movers of the day")
        stock_voice.speak("" + TOP_MOVERS[1]['symbol'] )
    if random_num == 2:
        stock_voice.speak("hi 2")
