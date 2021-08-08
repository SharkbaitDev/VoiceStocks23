import speech_recognition as sr

import stock_manager
import stock_price_manager
import stock_voice


# pip SpeechRecognition, PipWin(PyAudio), gTTS, playsound


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))
    return said


WAKE_LIST = ["hello there", "hey there", "hello", "hello abdul"]
PRICE_REQUEST_PHRASES_LIST = []
WAKE = "hello there"
sleep_mode = True
loaded = False

while True:

    if not loaded:
        loaded = True
        my_file = open("stock_price_request_phrases", "r")
        content = my_file.read()
        content_list = content.split(",")
        my_file.close()
        for phrase in content_list:
            PRICE_REQUEST_PHRASES_LIST.append(phrase.replace("'", "").replace("[", "").replace("]", "").replace("-", ""))

    if sleep_mode:
        text = get_audio()
    for wake in WAKE_LIST:
        if text.count(wake.lower()) > 0 or not sleep_mode:
            if sleep_mode:
                stock_voice.speak("What can I do?")

            sleep_mode = False
            new_text = get_audio()
            sample_text = new_text
            new_text = ""
            stock = ""
            split_text = sample_text.split()
            count = 0
            caps_text = ""
            for words in split_text:
                print("checking for stock: " + words)
                try:
                    print(str(stock_manager.get_live_price(words)))
                    if stock_manager.get_live_price(words) is int:
                        if words == "is" or words[1] == "is":
                            continue
                        stock = words
                        if words.upper():
                            caps_text = words
                        if len(caps_text) > 0:
                            stock = caps_text
                except KeyError as k:
                    print("key error: could not find: " + words)
                except AssertionError as e:
                    print("assertion error: could not find: " + words)

                #if stock_manager.get_live_price(words) is not None:
                #    stock = words
                #    break

            if len(stock) == 0:
                print("No stock found.")
            else:
                # Price Request
                for price_request_text in PRICE_REQUEST_PHRASES_LIST:
                    print("non-replaced: " + price_request_text)
                    price_request_text = price_request_text.replace("{stock}", stock)
                    print("replaced: " + price_request_text)
                    print("said:" + sample_text)
                    if price_request_text in sample_text:
                        print("3")
                        stock_price_manager.say_price(stock)

                #if "what is the price of " in sample_text:
                #    stock = sample_text.split()[5]
                #    stock_price_manager.say_price(stock)

                print(f"Recognized {sample_text}")
                continue