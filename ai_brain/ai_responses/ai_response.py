import json
import ruamel.yaml

RESPONSE_LIST = []

OKAY_LIST = []
SENTIMENT_ANALYSIS_ASK = []
STOCK_PRICE_ANSWER_INTEGER = []
STOCK_PRICE_ANSWER_DECIMAL = []


def load_essential_answers():
    # LOAD NO PHRASES

    with open('input.yaml') as fp:
        str_data = fp.read()
    data = ruamel.yaml.load(str_data)



load_essential_answers()