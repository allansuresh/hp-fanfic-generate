<<<<<<< HEAD
=======
#import all required packages, such as numpy, pandas, nltk  
#venv folder in the repo contains all these and more
import numpy as np
import pandas as pd
import os
import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
>>>>>>> d7de3abbf1ca39b7bc805b41a26ec665903f7ba0
import random

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
