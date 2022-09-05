import difflib
from news import stock_individual_news

STOCK_ADVICE_PHRASES = []

def load_phrases():
    with open("advice/stock_individual_advice_phrases", "r") as f:
        for line in f:
            STOCK_ADVICE_PHRASES.append(
                line.strip().replace("'", "").replace("[", "").replace("]", "").replace("-", ""))

def init_advice_manager(msg):
    appended_stock = ""
    final_key = ""
    break_statement = False
    for price_request_text in STOCK_ADVICE_PHRASES:
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
    research(final_key)

def research(stock):
    stock_individual_news.get_news_without_printing(stock)
    pros = []
    cons = []

    for str in stock_individual_news.sentences:
        if "Top Tech" in str:
            pros.append("- Rated in top 10 stock picks")
            continue
        elif "Stocks to Buy" in str:
            pros.append("- Rated in stocks to buy")
            continue
        elif "Tech Top" in str:
            pros.append("- Rated in top tech stock picks")
            continue

        elif "Downfall" in str:
            cons.append("")


