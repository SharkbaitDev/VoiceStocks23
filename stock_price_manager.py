import math
import random
import stock_manager
import stock_voice
import os
import sys


def say_price(stock):
    random_num = random.randint(1, 5)

    unrounded_price = stock_manager.get_live_price(stock)
    price = round(unrounded_price, 2)

    if float(price).is_integer():
        if random_num == 1:
            stock_voice.speak("The price of " + stock + " is currently " + str(price) + " dollars")
        elif random_num == 2:
            stock_voice.speak("Currently, " + stock + " is at " + str(price) + " dollars")
        elif random_num == 3:
            stock_voice.speak(stock + " is at " + str(price) + " dollars right now")
        elif random_num == 4:
            stock_voice.speak("As of right now, " + stock + " is at " + str(price) + " dollars")
        elif random_num == 5:
            stock_voice.speak(str(price) + " dollars.")
    else:
        new_cents_price = str(round(math.modf(price)[0], 2)).replace("0.", "")
        dollars_price = math.trunc(price)
        if random_num == 1:
            #print("stock: " + stock)
            #print("str(price): " + str(price))
            #print("str(new_cents_price): " + str(new_cents_price))
            stock_voice.speak("The price of " + stock + " is " + str(dollars_price) + " dollars and " + new_cents_price + " cents")

        elif random_num == 2:
            stock_voice.speak("Currently, " + stock + " is at " + str(dollars_price) + " dollars and " + new_cents_price + " cents")

        elif random_num == 3:
            stock_voice.speak(stock + " is at " + str(dollars_price) + " dollars and " + new_cents_price + " cents right now")

        elif random_num == 4:
            stock_voice.speak("As of right now, " + stock + " is at " + str(dollars_price) + " dollars and " + new_cents_price + " cents")

        elif random_num == 5:
            stock_voice.speak(str(dollars_price) + " dollars and " + new_cents_price + " cents")
