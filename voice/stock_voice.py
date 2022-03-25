import os
from gtts import gTTS
import playsound
import random
import pyttsx3 as tts
import speech_recognition as sr

speaker = tts.init()
speaker.setProperty('rate', 150)
voice_id = "com.apple.speech.synthesis.voice.samantha"
speaker.setProperty('voice', voice_id)
voices = speaker.getProperty('voices')
#for voice in voices:
#    print("id: " + voice.id)
#    speaker.setProperty('voice', voice.id)
#    speaker.say('The quick brown fox jumped over the lazy dog.')
#    speaker.runAndWait()
    # Karen
    # Samantha
    # Victoria MAYBE

# voices = speaker.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")
#for voice in voices:
#    print("id: " + voice.id)
#    speaker.setProperty('voice', voice.id)
#    # engine.say('The quick brown fox jumped over the lazy dog.')
#    speaker.say("Hello, I am robot")
#speaker.runAndWait()

def speak(msg):
    speaker.say(msg)
    print(msg)
    speaker.runAndWait()


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

def legacy_speak(msg):
    gtts = gTTS(text=msg, lang="en", slow=False)
    rand_num = random.randint(1, 99999999)
    filename = "voice-" + str(rand_num) + ".mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)
