import difflib

import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

from ai_brain import essential_answers
from voice import stock_voice

nltk.download('vader_lexicon')

STOCK_INDIVIDUAL_NEWS = []


def load_phrases():
    with open("news/stock_individual_news_phrases", "r") as f:
        for line in f:
            STOCK_INDIVIDUAL_NEWS.append(
                line.strip().replace("'", "").replace("[", "").replace("]", "").replace("-", ""))

sentences = []
sdf = []
global_parsed_news = []
global_ticker = ""


def get_news_without_printing(ticker):
    # Parameters
    n = 5  # the # of article headlines displayed per ticker
    tickers = ticker

    # Get Data
    finwiz_url = 'https://finviz.com/quote.ashx?t='
    news_tables = {}

    url = finwiz_url + ticker
    req = Request(url=url, headers={'user-agent': 'my-app/0.0.1'})
    resp = urlopen(req)
    html = BeautifulSoup(resp, features="lxml")
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table

    try:
        df = news_tables[ticker]
        df_tr = df.findAll('tr')

        print('\n')
        print('Recent News Headlines for {}: '.format(ticker))

        for i, table_row in enumerate(df_tr):
            a_text = table_row.a.text
            td_text = table_row.td.text
            td_text = td_text.strip()
            print(a_text, '(', td_text, ')')
            sentences.append(a_text + " (" + td_text + ")")
            if i == n - 1:
                break
    except KeyError:
        pass

    # Iterate through the news
    parsed_news = []
    for file_name, news_table in news_tables.items():
        for x in news_table.findAll('tr'):
            text = x.a.get_text()
            date_scrape = x.td.text.split()

            if len(date_scrape) == 1:
                time = date_scrape[0]

            else:
                date = date_scrape[0]
                time = date_scrape[1]

            ticker = file_name.split('_')[0]

            parsed_news.append([ticker, date, time, text])

    # Sentiment Analysis
    analyzer = SentimentIntensityAnalyzer()

    columns = ['Ticker', 'Date', 'Time', 'Headline']
    news = pd.DataFrame(parsed_news, columns=columns)
    scores = news['Headline'].apply(analyzer.polarity_scores).tolist()

    df_scores = pd.DataFrame(scores)
    news = news.join(df_scores, rsuffix='_right')

    # View Data
    news['Date'] = pd.to_datetime(news.Date).dt.date

    unique_ticker = news['Ticker'].unique().tolist()
    news_dict = {name: news.loc[news['Ticker'] == name] for name in unique_ticker}

    values = []
    dataframe = news_dict[ticker]
    dataframe = dataframe.set_index('Ticker')
    dataframe = dataframe.drop(columns=['Headline'])
    print('\n')
    print(dataframe.head())

    mean = round(dataframe['compound'].mean(), 2)
    values.append(mean)

    df = pd.DataFrame(list(zip(tickers, values)), columns=['Ticker', 'Mean Sentiment'])
    df = df.set_index('Ticker')
    df = df.sort_values('Mean Sentiment', ascending=False)
    print('\n')
    print(df)
    sdf = df

def get_news(ticker):
    # Parameters
    n = 5  # the # of article headlines displayed per ticker
    tickers = ticker
    sentences = []
    global_parsed_news.clear()
    stock_voice.speak("Here are the 5 most recent headlines regarding " + ticker)

    # Get Data
    finwiz_url = 'https://finviz.com/quote.ashx?t='
    news_tables = {}

    url = finwiz_url + ticker
    req = Request(url=url, headers={'user-agent': 'my-app/0.0.1'})
    resp = urlopen(req)
    html = BeautifulSoup(resp, features="lxml")
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table

    try:
        df = news_tables[ticker]
        df_tr = df.findAll('tr')

        print('\n')
        print('Recent News Headlines for {}: '.format(ticker))

        for i, table_row in enumerate(df_tr):
            a_text = table_row.a.text
            td_text = table_row.td.text
            td_text = td_text.strip()
            print(a_text, '(', td_text, ')')
            sentences.append(a_text + " (" + td_text + ")")
            stock_voice.speak(a_text)
            if i == n - 1:
                break
    except KeyError:
        pass

    # Iterate through the news
    parsed_news = []
    for file_name, news_table in news_tables.items():
        for x in news_table.findAll('tr'):
            text = x.a.get_text()
            date_scrape = x.td.text.split()

            if len(date_scrape) == 1:
                time = date_scrape[0]

            else:
                date = date_scrape[0]
                time = date_scrape[1]

            ticker = file_name.split('_')[0]

            parsed_news.append([ticker, date, time, text])
            global_parsed_news.append([ticker, date, time, text])

    stock_voice.speak("Would you like me to conduct sentiment analysis on each of these headlines?")

    answer = stock_voice.get_audio()


    if essential_answers.check_text_for_answer(answer, "yes"):
        stock_voice.speak("Conducting sentiment analysis...")
        conduct_sentiment_analysis(tickers)

        stock_voice.speak("Would you like me to go more in depth? ")
        return
    elif essential_answers.check_text_for_answer(answer, "no"):
        stock_voice.speak("Alright.")
        return


def conduct_sentiment_analysis(tickers):
    # Sentiment Analysis
    analyzer = SentimentIntensityAnalyzer()

    columns = ['Ticker', 'Date', 'Time', 'Headline']
    news = pd.DataFrame(global_parsed_news, columns=columns)
    scores = news['Headline'].apply(analyzer.polarity_scores).tolist()

    df_scores = pd.DataFrame(scores)
    news = news.join(df_scores, rsuffix='_right')

    # View Data
    news['Date'] = pd.to_datetime(news.Date).dt.date

    unique_ticker = news['Ticker'].unique().tolist()
    news_dict = {name: news.loc[news['Ticker'] == name] for name in unique_ticker}

    values = []
    dataframe = news_dict[tickers]
    dataframe = dataframe.set_index('Ticker')
    dataframe = dataframe.drop(columns=['Headline'])
    print('\n')
    print(dataframe.head())

    mean = round(dataframe['compound'].mean(), 2)
    values.append(mean)

    df = pd.DataFrame(list(zip(tickers, values)), columns=['Ticker', 'Mean Sentiment'])
    df = df.set_index('Ticker')
    df = df.sort_values('Mean Sentiment', ascending=False)
    print('\n')
    print(df)

    stock_voice.speak("The final mean sentiment is " + str(df._get_value('Mean Sentiment')) + ".")

def init_news_manager(msg):
    appended_stock = ""
    final_key = ""
    break_statement = False
    for price_request_text in STOCK_INDIVIDUAL_NEWS:
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
    get_news(final_key)

#get_news("MSFT")