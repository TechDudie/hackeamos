from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

metadata = lambda level: f"[Hackeamos] [{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[11:-3]}] [{level}]"

def log(message: str, level="INFO"):
    print(f"{metadata(level)} {message}")

URL = "https://conjuguemos.com/"

PRONOUNS = ["yo", "tú", "él ella usted", "nosotros", "vosotros", "ellos ellas ustedes"]
ENDINGS = {
    "ar": ["o", "as", "a", "amos", "áis", "an"],
    "er": ["o", "es", "e", "emos", "éis", "en"],
    "ir": ["o", "es", "e", "imos", "ís", "en"]
}

with open("irregular_verbs.csv") as file: VERBS = file.read().strip().split("\n")
VERB_KEYS = [verb.split(",")[0] for verb in VERBS]

log("Irregular verbs loaded:")
for verbs in VERBS:
    verb = verbs.split(",")
    log(f"{verb[0]}: {str(verb[1:])}")

driver = webdriver.Chrome()
driver.get(URL)


questions = int(input(f"{metadata('INFO')} How many questions to complete?"))
input(f"{metadata('INFO')} === Press Enter to launch answer bot ===")

pronoun = driver.find_element(by=By.ID, value="pronoun-input")
verb = driver.find_element(by=By.ID, value="verb-input")
answer = driver.find_element(by=By.ID, value="assignment-answer-input")

for i in range(questions + 1):
    if pronoun.text.find("-") != -1 or verb.text.find("-") != -1:
        break

    pronoun_index = 0
    if pronoun.text.find(" y ") != -1:
        if pronoun.text.find("yo") != -1:
            pronoun_index = 3
        else:
            pronoun_index = 5
    else:
        x = 0
        recognized = False
        for i in PRONOUNS:
            if i.find(pronoun.text) != -1:
                pronoun_index = x
                recognized = True
                break
            x += 1
        if not recognized:
            pronoun_index = 2

    if verb.text in VERB_KEYS:
        index = VERB_KEYS.index(verb.text)
        result = VERBS[index].split(",")[pronoun_index + 1]
    else:
        result = verb.text[:-2] + ENDINGS[verb.text[-2:]][pronoun_index]
    
    log(f"Pronoun: {pronoun.text} Verb: {verb.text} Conjugation: {result}")

    try:
        answer.send_keys(result)
        answer.send_keys(Keys.ENTER)
    except:
        break

input(f"{metadata('INFO')} === Assignment complete, press Enter to terminate ===")