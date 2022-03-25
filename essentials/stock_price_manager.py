import math
import random

from util import stock_manager
from voice import stock_voice
import difflib

PRICE_REQUEST_PHRASES_LIST = []
COMPANY_NAMES = []


# print(stock_manager.getName("SCCO"))

def find_stock_keyword(test_str, K):
    res = ''
    for idx in range(K, len(test_str)):
        if test_str[idx] == ' ':
            break
        res += test_str[idx]


def load_phrases():
    with open("essentials/stock_price_request_phrases", "r") as f:
        for line in f:
            PRICE_REQUEST_PHRASES_LIST.append(
                line.strip().replace("'", "").replace("[", "").replace("]", "").replace("-", ""))
            # print("phrase: '" + line.strip() + "'")


def load_ease_company_names():
    with open("essentials/stock_price_request_ease_company_names", "r") as f:
        for line in f:
            COMPANY_NAMES.append(
                line.strip().replace("'", "").replace("[", "").replace("]", "").replace("-", ""))
            # print("phrase: '" + line.strip() + "'")


def init_stock_price_request(msg):
    appended_stock = ""
    final_key = ""
    break_statement = False
    for price_request_text in PRICE_REQUEST_PHRASES_LIST:
        print('{} => {}'.format(price_request_text, msg))
        generated_initial_key = False
        initial_key = 0
        for i, s in enumerate(difflib.ndiff(price_request_text, msg)):
            if s[0] == ' ':
                continue
            elif s[0] == '-':
                print(u'Delete "{}" from position {}'.format(s[-1], i))
            elif s[0] == '+':
                print(u'Add "{}" to position {}'.format(s[-1], i))
                appended_stock = appended_stock + s[-1]
                # print(appended_stock)
            try:
                res = ""
                if not generated_initial_key:
                    generated_initial_key = True
                    initial_key = i
                    res = msg[i:].split()[0]
                    if msg[i - 1] != " ":
                        print("11: " + msg[i - 1])
                        res = msg[i - 1:].split()[0]
                    elif msg[i - 2] != " ":
                        print("22: " + msg[i - 2])
                        res = msg[i - 2:].split()[0]
                    price_request_text2 = price_request_text.replace("{stock}", str(res)).lower()
                    msg = msg.lower()
                    print("res: " + str(res) + " (" + str(i) + ")")
                    print("req2: '" + price_request_text2 + "'")
                    print("original: '" + msg + "'")

                    if price_request_text2 == msg:
                        final_key = str(res)
                        print("Final Key Found! Key: " + final_key)
                        break_statement = True
                        break
                elif generated_initial_key:
                    res = msg[initial_key:].split()[0]
                    if msg[initial_key - 1] != " ":
                        print("11: " + msg[initial_key - 1])
                        res = msg[initial_key - 1:].split()[0]
                    # elif msg[initial_key-2] != " ":
                    #    print("22: " + msg[initial_key-2])
                    #    res = msg[initial_key-2:].split()[0]
                    price_request_text2 = price_request_text.replace("{stock}", str(res)).lower()
                    msg = msg.lower()
                    print("res: " + str(res) + " (" + str(initial_key) + ")")
                    print("req2: '" + price_request_text2 + "'")
                    print("original: '" + msg + "'")

                    if price_request_text2 == msg:
                        final_key = str(res)
                        print("Final Key Found! Key: " + final_key)
                        break
            finally:
                if break_statement:
                    break
                else:
                    continue
        if break_statement:
            break
    print("final key 2: " + final_key)
    say_price(final_key)


def say_price(stock):
    random_num = random.randint(1, 5)

    if stock_manager.get_live_price(stock) is None:
        stock_voice.speak("Unfortunately, I could not find that stock. Try saying the ticker name. ")
        return

    for phrase in COMPANY_NAMES:
        substring = phrase.split("|")

        # 0 = long name
        # 1 = ticker

        if stock == substring[0]:
            stock = substring[1]
            continue
        continue

    unrounded_price = stock_manager.get_live_price(stock)

    price = round(unrounded_price, 2)

    if float(price).is_integer():
        if random_num == 1:
            stock_voice.speak(
                "The price of " + stock_manager.getName(stock) + " is currently " + str(price) + " dollars")
        elif random_num == 2:
            stock_voice.speak("Currently, " + stock_manager.getName(stock) + " is at " + str(price) + " dollars")
        elif random_num == 3:
            stock_voice.speak(stock_manager.getName(stock) + " is at " + str(price) + " dollars right now")
        elif random_num == 4:
            stock_voice.speak("As of right now, " + stock_manager.getName(stock) + " is at " + str(price) + " dollars")
        elif random_num == 5:
            stock_voice.speak(str(price) + " dollars.")
    else:
        new_cents_price = str(round(math.modf(price)[0], 2)).replace("0.", "")
        dollars_price = math.trunc(price)
        if random_num == 1:
            stock_voice.speak(
                "The price of " + stock_manager.getName(stock) + " is " + str(
                    dollars_price) + " dollars and " + new_cents_price + " cents")

        elif random_num == 2:
            stock_voice.speak(
                "Currently, " + stock_manager.getName(stock) + " is at " + str(
                    dollars_price) + " dollars and " + new_cents_price + " cents")

        elif random_num == 3:
            stock_voice.speak(
                stock_manager.getName(stock) + " is at " + str(
                    dollars_price) + " dollars and " + new_cents_price + " cents right now")

        elif random_num == 4:
            stock_voice.speak("As of right now, " + stock_manager.getName(stock) + " is at " + str(
                dollars_price) + " dollars and " + new_cents_price + " cents")

        elif random_num == 5:
            stock_voice.speak(str(dollars_price) + " dollars and " + new_cents_price + " cents")
