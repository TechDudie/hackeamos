import json

PRONOUNS = [
    ["yo"],
    ["tú"],
    ["él", "ella", "usted"],
    ["nosotros", "nosotras"],
    ["vosotros", "vosotras"],
    ["ellos", "ellas", "ustedes"]
]

ENDINGS = {
    "ar": ["o", "as", "a", "amos", "áis", "an"],
    "er": ["o", "es", "e", "emos", "éis", "en"],
    "ir": ["o", "es", "e", "imos", "ís", "en"]
}

data = json.load(open("verbs.json"))

find = lambda a, b: b.find(a) != -1
pronoun = lambda noun: (3 if find(" y ", noun) else 0) + (0 if find("yo", noun) else (1 if find("tú", noun) else 2))
goyo = lambda verb, pronoun_index, irregular_yo: ((verb[:-2] + "go") if irregular_yo == "" else irregular_yo) if pronoun_index == 0 else (verb[:-2] + ENDINGS[verb[-2:]][pronoun_index])

def stem_changing(verb, pronoun_index, change_rule):
    stem = verb[:-2]
    k = stem.rfind(change_rule.split(" ")[0])
    return (stem[:k] + change_rule.split(" ")[1] + stem[k + 1:] + ENDINGS[verb[-2:]][pronoun_index]) if pronoun_index != 3 else (stem + ENDINGS[verb[-2:]][3])

def pronoun(noun):
    if find(" y ", noun):
        if find("yo", noun):
            return 3
        if find("tú", noun):
            return 4
        else:
            return 5
    else:
        for i in range(len(PRONOUNS)):
            if noun in PRONOUNS[i]:
                return i
        return 2

def conjugate(verb, noun):
    pronoun_index = pronoun(noun)

    if verb in data["irregular"].keys():
        return data["irregular"][verb][pronoun_index]
    
    if verb in data["stem_changing"].keys():
        return stem_changing(verb, pronoun_index, data["stem_changing"][verb])
    
    if verb in data["goyo"].keys():
        return goyo(verb, pronoun_index, data["goyo"][verb])
    
    return verb[:-2] + ENDINGS[verb[-2:]][pronoun_index]

if __name__ == "__main__":
    while True:
        noun = input("Noun: ")
        verb = input("Verb: ")
        print("Conjugation: " + conjugate(verb, noun))