import speech_recognition as sr

import stock_advice_manager
import stock_individual_news
import stock_price_manager
import stock_voice
from difflib import SequenceMatcher
import stock_dailymovers
import robin_stocks
from robin_stocks import robinhood as rs
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import self
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
# pip SpeechRecognition, PipWin(PyAudio), gTTS, playsound

# MACHINE LEARNING LOAD

nltk.download('punkt')
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json').read())

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))


classes = sorted(set(classes))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)

train_x = list(training[:, 0])
train_y = list(training[:, 1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),),activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.h5', hist)


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


WAKE_LIST = ["hello there", "hey there", "hello"]
WAKE = "hello there"
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
        loaded = True

    if sleep_mode:
        text = get_audio()
    for wake in WAKE_LIST:
        if text.count(wake.lower()) > 0 or not sleep_mode:
            if sleep_mode:
                stock_voice.speak("Hello.")

            sleep_mode = False
            new_text = get_audio()

            for phrase in stock_price_manager.PRICE_REQUEST_PHRASES_LIST:
                if similar(new_text, phrase) > 0.75:
                    stock_price_manager.init_stock_price_request(new_text)
                    break
            for phrase_movers in stock_dailymovers.DAILYMOVERS_REQUEST_LIST:
                if similar(new_text, phrase_movers) > 0.75:
                    stock_dailymovers.init_dailymovers_request()
                    break
            for phrase_advice in stock_advice_manager.STOCK_ADVICE_PHRASES:
                if similar(new_text, phrase_advice) > 0.75:
                    stock_advice_manager.init_advice_manager(new_text)
            for phrase_individual_news in stock_individual_news.STOCK_INDIVIDUAL_NEWS:
                if similar(new_text, phrase_individual_news) > 0.75:
                    stock_individual_news.init_news_manager(new_text)