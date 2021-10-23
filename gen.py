#import all required packages, such as numpy, pandas, nltk  
#venv folder in the repo contains all these and more
import numpy as np
import pandas as pd
import os
import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import random
from pathlib import Path


#Read the Harry Potter input file
stories = []
for _, _, files in os.walk("C:\\Users\\allan\Documents\GitHub\hp-fanfic-generate\\"):
    for file in files:
        with open("C:\\Users\\allan\Documents\GitHub\hp-fanfic-generate\hp_poa.txt") as f:
            for line in f:
                line = line.strip()
                if line=='----------': break
                if line!='':stories.append(line)

#stories = stories.replace('\n',' ')


#Clean the data
def clean_txt(txt):
    cleaned_txt = []
    for line in txt:
        line = line.lower()
        line = re.sub(r"[,.\"\'!@#$%^&*(){}?/;`~:<>+=-\\]", "", line)
        tokens = word_tokenize(line)
        words = [word for word in tokens if word.isalpha()]
        cleaned_txt+=words
    return cleaned_txt

cleaned_stories = clean_txt(stories)


#Create Markov model
def make_markov_model(cleaned_stories, n_gram=5):
    markov_model = {}
    for i in range(len(cleaned_stories)-n_gram-4):
        curr_state, next_state = "", ""
        for j in range(n_gram):
            curr_state += cleaned_stories[i+j] + " "
            next_state += cleaned_stories[i+j+n_gram] + " "
        curr_state = curr_state[:-1]
        next_state = next_state[:-1]
        if curr_state not in markov_model:
            markov_model[curr_state] = {}
            markov_model[curr_state][next_state] = 1
        else:
            if next_state in markov_model[curr_state]:
                markov_model[curr_state][next_state] += 1
            else:
                markov_model[curr_state][next_state] = 1

    # calculating transition probabilities
    for curr_state, transition in markov_model.items():
        total = sum(transition.values())
        for state, count in transition.items():
            markov_model[curr_state][state] = count/total
    return markov_model

markov_model = make_markov_model(cleaned_stories)


#Generate fanfic stories
def generate_story(markov_model, start, limit=100):
    n = 0
    curr_state = start
    next_state = None
    story = ""
    story+=curr_state+" "
    while n<limit:
        next_state = random.choices(list(markov_model[curr_state].keys()), list(markov_model[curr_state].values()))

        curr_state = next_state[0]
        story+=curr_state+" "
        n+=1
    return story

print(generate_story(markov_model, start='harry was', limit=100))
