from yahoo_fin import stock_info as si
import yfinance as yf

def get_live_price(stock):
    return si.get_live_price(stock)

def get_day_gainers():
    return si.get_day_gainers()


def get_day_losers():
    return si.get_day_losers()


def get_most_active():
    return si.get_day_most_active()

def getName(stock):
    st = yf.Ticker(stock)
    name = st.info['longName']
    return name

def getInfo(stock):
    st = yf.Ticker(stock)
    name = st.info['longBusinessSummary']
    return name