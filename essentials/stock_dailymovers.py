import pandas as pd
import random
import yfinance as yf

from util import stock_manager
from voice import stock_voice

DAILYMOVERS_REQUEST_LIST = []
TOP_MOVERS = []

def load_phrases():
    with open("essentials/stock_dailymovers_request", "r") as f:
        for line in f:
            DAILYMOVERS_REQUEST_LIST.append(
                line.strip().replace("'", "").replace("[", "").replace("]", "").replace("-", ""))
