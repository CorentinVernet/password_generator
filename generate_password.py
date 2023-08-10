from tkinter import Tk, Label, Button
from random import random, choice
import json
from pattern.text.fr import conjugate, pluralize, SINGULAR, PLURAL, INFINITIVE, PRESENT

def randomize_pluralization(noun):
    number = random()
    if (number >= 0.5):
        return [pluralize(noun), PLURAL]
    else:
        return [noun, SINGULAR]

def calculate_article(noun, gender, number):
    if (number == PLURAL):
        return "Les "
    elif ("aeiouy".find(noun[0]) > -1):
        return "L\'"
    elif (gender == "m"):
        return "Le "
    else:
        return "La "

def pattern_stopiteration_workaround():
    try: conjugate('lorem ipsum', INFINITIVE)
    except: pass

def read_words(filename, word_type):
    with open(filename, 'r', -1, 'utf-8') as json_file:
       data = json.load(json_file)
       return data[word_type]

def generate_password(password_label, copied_to_clipboard_label):
    copied_to_clipboard_label['text'] = ""

    subjects = read_words("assets\\common_nouns.json", "nouns")
    verbs = read_words("assets\\common_verbs.json", "verbs")
    complements = read_words("assets\\common_nouns.json", "nouns")
    adjectives = read_words("assets\\common_adjectives.json", "adjectives")
    ponctuations = ['!','?']


    #### SUBJECT ####
    subject = choice(subjects) # Object
    [pluralized_subject, subject_number] = randomize_pluralization(subject['noun'])
    subject_article = calculate_article(pluralized_subject, subject["gender"], subject_number)
    formatted_subject = subject_article + pluralized_subject

    ### VERB ###
    verb = choice(verbs) # String
    pattern_stopiteration_workaround()
    conjugated_verb = conjugate(verb, PRESENT, 3, subject_number)

    ### COMPLEMENT ###
    complement = choice(complements) # Object
    [pluralized_complement, complement_number] = randomize_pluralization(complement['noun'])
    complement_article = calculate_article(pluralized_complement, complement["gender"], complement_number).lower()
    formatted_complement = complement_article + pluralized_complement

    ### ADJECTIVE ###
    adjective = choice(adjectives) # Object
    if (complement['gender'] == 'm'):
        gendered_adjective = adjective['masculine']
    else:
        gendered_adjective = adjective['feminine']
    if (complement_number == PLURAL):
        gendered_adjective = pluralize(gendered_adjective) 

    ### PONCTUATION ###
    ponctuation = choice(ponctuations)

    password_label["text"] = f"{formatted_subject} {conjugated_verb} {formatted_complement} {gendered_adjective.lower()} {ponctuation}"

def copy_to_clipboard(root, password, copied_to_clipboard_label):
    if (password != ""):
        root.clipboard_clear()
        root.clipboard_append(password)
        copied_to_clipboard_label["text"] = "Copié !"


if __name__ == "__main__":
    root = Tk()
    root.title("Générateur de mots de passe")
    root.geometry("300x200")
    password_label = Label(root, text="")
    copied_to_clipboard_label = Label(root, text="")
    generate_button = Button(root, text="Générer un mot de passe", command=lambda : generate_password(password_label, copied_to_clipboard_label))
    generate_button.pack(pady=20)
    password_label.pack() 
    copy_to_clipboard_button = Button(root, text="Copier dans le presse-papiers", command=lambda: copy_to_clipboard(root, password_label['text'], copied_to_clipboard_label))  
    copy_to_clipboard_button.pack(pady=20)
    copied_to_clipboard_label.pack()
    
    root.mainloop()