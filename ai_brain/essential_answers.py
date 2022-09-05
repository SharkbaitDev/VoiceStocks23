import random

NO_ANSWER_LIST = []
YES_ANSWER_LIST = []
ACKNOWLEDGE_LIST = []

def load_essential_answers():
    # LOAD NO PHRASES
    with open("ai_brain/human_answers/essential_answer_no", "r") as f:
        for line in f:
            NO_ANSWER_LIST.append(
                line.strip().replace("'", "").replace("[", "").replace("]", "").replace("-", ""))

    with open("ai_brain/human_answers/essential_answer_yes", "r") as f:
        for line in f:
            YES_ANSWER_LIST.append(
                line.strip().replace("'", "").replace("[", "").replace("]", "").replace("-", ""))
    with open("ai_brain/human_answers/essential_answer_acknowledge", "r") as f:
        for line in f:
            ACKNOWLEDGE_LIST.append(
                line.strip().replace("'", "").replace("[", "").replace("]", "").replace("-", ""))


# Check the inputted voice audio for "yes" or "no"
def check_text_for_answer(text, phrase_id):
    if phrase_id is "no":
        for phrase in NO_ANSWER_LIST:
            if phrase is text.lower():
                return True
            elif phrase not in text.lower():
                return False
    elif phrase_id is "yes":
        for phrase in YES_ANSWER_LIST:
            if phrase is text.lower():
                return True
            elif phrase not in text.lower():
                return False
    else:
        print("could not find phrase id. error 1")

def random_no():
    index = ACKNOWLEDGE_LIST.count()

    rand = random.randint(index)

    return ACKNOWLEDGE_LIST[rand]
