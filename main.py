from argparse import ArgumentParser
from datetime import datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import conjugate

metadata = lambda level: f"[Hackeamos] [{datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]}] [{level}]"

def log(message: str, level="INFO"):
    print(f"{metadata(level)} {message}")

URL = "https://conjuguemos.com/"
URL_AUTH = "https://conjuguemos.com/auth/oauth2/google"

if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("-e", "--email", help="Email")
    parser.add_argument("-p", "--password", help="Password")

    parser.add_argument("-i", "--infinite", action="store_true", help="Enable infinite questions")
    parser.add_argument("-s", "--self", action="store_true", help="Enable self-practice mode")

    parser.add_argument("-c", "--count", type=int, help="Number of questions to answer")

    args = parser.parse_args()

    driver = webdriver.Chrome()
    driver.get(URL)

    if args.email is not None or args.password is not None:
        driver.get(URL_AUTH)

        google_email = driver.find_element(by=By.ID, value="identifierId")
        google_email.send_keys(args.email)
        google_email.send_keys(Keys.ENTER)
        sleep(2)

        try:
            microsoft_email = driver.find_element(by=By.ID, value="i0116")
            microsoft_email.send_keys(args.email)
            microsoft_email.send_keys(Keys.ENTER)
            sleep(2)

            microsoft_password = driver.find_element(by=By.ID, value="i0118")
            microsoft_password.send_keys(args.password)
            microsoft_password.send_keys(Keys.ENTER)
            sleep(1)
        except:
            google_password = driver.find_elements(by=By.NAME, value="Passwd")[0]
            google_password.send_keys(args.password)
            google_password.send_keys(Keys.ENTER)
            sleep(1)

        try:
            driver.find_elements(By.CLASS_NAME, "VfPpkd-LgbsSe-OWXEXe-dgl2Hf")[0].click()
        except:
            pass

        sleep(2)
        input(f"{metadata('INFO')} === Press Enter to launch answer bot ===")

    else:
        driver.get(URL)
        input(f"{metadata('INFO')} === Press Enter to launch answer bot ===")

    try:
        pronoun = driver.find_element(by=By.ID, value="pronoun-input")
        verb = driver.find_element(by=By.ID, value="verb-input")
        if args.self:
            answer = driver.find_element(by=By.ID, value="answer-input")
        else:
            answer = driver.find_element(by=By.ID, value="assignment-answer-input")
    except:
        log("Unable to access assignment metadata; do you have the correct page open?", "ERROR")
        exit()
    
    if not args.self:
        try:
            assignment_metadata = driver.find_elements(by=By.CLASS_NAME, value="fw--700")
            goal = int(assignment_metadata[0].text)
            attempts = int(assignment_metadata[1].text)
        except:
            log("Unable to access assignment metadata; do you have the correct page open?", "ERROR")
            exit()

    if args.self:
        count = args.count
    else:
        count = attempts
    
    for i in range(count):
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
