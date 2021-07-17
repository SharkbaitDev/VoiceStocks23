import os
from gtts import gTTS
import playsound
import random

def speak(msg):
    tts = gTTS(text=msg, lang="en", slow=False)
    rand_num = random.randint(1, 99999999)
    filename = "voice" + str(rand_num) + ".mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)