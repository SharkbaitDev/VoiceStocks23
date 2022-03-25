import pandas as pd
import random
import yfinance as yf

from util import stock_manager
from voice import stock_voice

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
    with open("essentials/stock_dailymovers_request", "r") as f:
        for line in f:
            DAILYMOVERS_REQUEST_LIST.append(
                line.strip().replace("'", "").replace("[", "").replace("]", "").replace("-", ""))


movementlist = []
for stock in df['Symbol']:
    # get history
    thestock = yf.Ticker(stock)
    hist = thestock.history(period="1d")
    # print(stock)
    low = float(10000)
    high = float(0)
    # print(thestock.info)
    for day in hist.itertuples(index=True, name='Pandas'):
        if day.Low < low:
            low = day.Low
        if high < day.High:
            high = day.High

    deltapercent = 100 * (high - low) / low
    Open = lookup_fn(hist, 0, "Open")
    # some error handling:
    if len(hist >= 5):
        Close = lookup_fn(hist, 4, "Close")
    else:
        Close = Open
    if (Open == 0):
        deltaprice = 0
    else:
        deltaprice = 100 * (Close - Open) / Open
    print(stock + " " + str(deltapercent) + " " + str(deltaprice))
    pair = [stock, deltapercent, deltaprice]
    movementlist.append(pair)

for entry in movementlist:
    if entry[1]>float(100):
        print(entry)

def say_top_movers():
    random_num = random.randint(1, 2)

    stock_voice.speak("Retrieving the top 5 movers of the day...")

    if random_num == 1:
        stock_voice.speak("Here are the top five movers of the day")
        stock_voice.speak("" + TOP_MOVERS[1]['symbol'])
    if random_num == 2:
        stock_voice.speak("hi 2")
