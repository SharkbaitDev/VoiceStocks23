import speech_recognition as sr

from advice import stock_advice_manager
from news import stock_individual_news
from essentials import stock_price_manager, stock_dailymovers
from voice import stock_voice
from difflib import SequenceMatcher
from ai_brain import essential_answers


# pip SpeechRecognition, PipWin(PyAudio), gTTS, playsound

# MACHINE LEARNING LOAD

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))
    return said


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


WAKE_LIST = []
with open("util/WAKE_LIST", "r") as f:
    for line in f:
        WAKE_LIST.append(line.strip().replace("'", "").replace("[", "").replace("]", "").replace("-", ""))

sleep_mode = True
loaded = False
test_mode = False
robinhood_auth = False

while True:

    # if test_mode:
    #    stock_price_manager.init_stock_price_request("price of csco")
    if not loaded:
        stock_price_manager.load_phrases()
        stock_dailymovers.load_phrases()
        stock_price_manager.load_ease_company_names()
        stock_individual_news.load_phrases()
        stock_advice_manager.load_phrases()
        essential_answers.load_essential_answers()
        loaded = True

    text = ""
    if sleep_mode:
        text = get_audio()
        print(text)
    for wake in WAKE_LIST:
        if text.count(wake.lower()) > 0 or not sleep_mode:
            if sleep_mode:
                stock_voice.speak("Hello, what can I do for you Mustafa?")

            sleep_mode = False
            new_text = get_audio()

            for phrase in stock_price_manager.PRICE_REQUEST_PHRASES_LIST:
                if similar(new_text, phrase) > 0.75:
                    stock_price_manager.init_stock_price_request(new_text)
                    break
            for phrase_movers in stock_dailymovers.DAILYMOVERS_REQUEST_LIST:
                if similar(new_text, phrase_movers) > 0.75:
                    # TODO: Stock daily movers
                    print("Daily movers!")
                    break
            for phrase_advice in stock_advice_manager.STOCK_ADVICE_PHRASES:
                if similar(new_text, phrase_advice) > 0.75:
                    stock_advice_manager.init_advice_manager(new_text)
            for phrase_individual_news in stock_individual_news.STOCK_INDIVIDUAL_NEWS:
                if similar(new_text, phrase_individual_news) > 0.75:
                    stock_individual_news.init_news_manager(new_text)
