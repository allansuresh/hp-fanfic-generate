#import all required packages
import numpy as np
import pandas as pd
import os
import re
import string
from pathlib import Path
from clean import clean_txt
from gen_markov_model import make_markov_model
from gen import generate_story


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

#Clean the data from the file
cleaned_text = clean_txt(stories)


#Create Markov model
markov_model = make_markov_model(cleaned_text)


print(generate_story(markov_model, start="harry heard", limit=100))
