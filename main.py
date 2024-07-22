from datetime import datetime
from random import randint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import conjugate

metadata = lambda level: f"[Hackeamos] [{datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]}] [{level}]"

def log(message: str, level="INFO"):
    print(f"{metadata(level)} {message}")

URL = "https://conjuguemos.com/"

driver = webdriver.Chrome()
driver.get(URL)

input(f"{metadata('INFO')} === Press Enter to launch answer bot ===")

try:
    pronoun = driver.find_element(by=By.ID, value="pronoun-input")
    verb = driver.find_element(by=By.ID, value="verb-input")
    answer = driver.find_element(by=By.ID, value="assignment-answer-input")

    assignment_metadata = driver.find_elements(by=By.CLASS_NAME, value="fw--700")
    goal = int(assignment_metadata[0].text)
    attempts = int(assignment_metadata[1].text)
except:
    log("Unable to access assignment metadata; do you have the correct page open?", "ERROR")
    exit()

for i in range(attempts):
    if pronoun.text.find("-") != -1 or verb.text.find("-") != -1:
        break

    conjugation = conjugate.conjugate(verb.text, pronoun.text)
    
    log(f"Pronoun: {pronoun.text} Verb: {verb.text} Conjugation: {conjugation}")

    try:
        answer.send_keys(conjugation)
        answer.send_keys(Keys.ENTER)

        try:
            driver.find_element(by=By.CLASS_NAME, value="incorrect")
            input(f"{metadata('INFO')} === Incorrect question, enter correct answer and press Enter ===")
        except:
            pass
    except:
        pass

input(f"{metadata('INFO')} === Assignment complete, press Enter to terminate ===")
