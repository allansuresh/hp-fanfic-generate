# build_model.py
import pickle
from pathlib import Path
from fanfic import read_input_file, clean_txt
from gen_markov_model import make_markov_model

def build_and_save_model(input_path, output_path):
    # Read the input text file
    stories = read_input_file(input_path)
    # Clean the text
    cleaned_text = clean_txt(stories)
    # Build the Markov model
    markov_model = make_markov_model(cleaned_text)
    
    # Save the model to disk
    with open(output_path, 'wb') as f:
        pickle.dump(markov_model, f)

if __name__ == "__main__":
    input_file = Path(__file__).parent / "hp.txt"
    output_file = Path(__file__).parent / "markov_model.pkl"
    build_and_save_model(input_file, output_file)
    print("Model built and saved successfully.")
