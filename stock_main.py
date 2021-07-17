import speech_recognition as sr
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


WAKE = "hello mustafa"
sleep_mode = True

while True:

    if sleep_mode:
        text = get_audio()
    if text.count(WAKE) > 0 or not sleep_mode:
        if sleep_mode:
            stock_voice.speak("What can I do?")

        sleep_mode = False
        new_text = get_audio()
        sample_text = new_text
        new_text = ""
        if "what is the price of " in sample_text:
            stock = sample_text.split()[5]
            stock_price_manager.say_price(stock)

        print(f"Recognized {sample_text}")
        continue
