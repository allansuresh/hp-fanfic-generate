# fanfic.py
import sys
from pathlib import Path
import os
from typing import List, Dict, Optional

# Import the components
from clean import clean_txt
from gen_markov_model import make_markov_model
from gen import generate_story

def read_input_file(input_file: Path) -> List[str]:
    """
    Read and validate the input file
    """
    stories = []
    try:
        with open(input_file) as f:
            for line in f:
                line = line.strip()
                if line == '----------':
                    break
                if line != '':
                    stories.append(line)
        
        if not stories:
            raise ValueError("No stories found in input file")
        
        return stories
    
    except Exception as e:
        raise Exception(f"Error reading input file: {str(e)}")
    
    pass

def enhance_story(story: str) -> str:
    """
    Enhance the generated story with better formatting
    """
    # Fix spacing around punctuation
    story = ' '.join(story.split())  # Normalize spacing
    story = story.replace(" .", ".").replace(" ,", ",").replace(" !", "!").replace(" ?", "?")
    
    # Capitalize sentences
    sentences = story.split(". ")
    sentences = [s.capitalize() for s in sentences if s]
    story = ". ".join(sentences)
    
    # Ensure proper ending
    if not story.endswith((".", "!", "?")):
        story += "."
        
    return story

    pass

def generate_fanfic(start_phrase: str, word_limit: int, markov_model) -> str:
    """
    Main function to generate fan fiction with improved error handling and formatting
    """
    try:
        # Generate story with improved formatting
        raw_story = generate_story(markov_model, start=start_phrase, limit=word_limit)
        enhanced_story = enhance_story(raw_story)
        
        return enhanced_story

    except Exception as e:
        error_msg = f"Error generating story: {str(e)}"
        print(error_msg)
        return error_msg
    
    pass

def parse_arguments() -> tuple:
    """
    Parse and validate command line arguments
    """
    # Get start phrase and word limit from command line arguments
    start_phrase = sys.argv[1] if len(sys.argv) > 1 else "harry potter"
    
    try:
        word_limit = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        if word_limit <= 0:
            print("Warning: Word limit must be positive. Using default value of 100.")
            word_limit = 100
    except ValueError:
        print("Warning: Invalid word limit. Using default value of 100.")
        word_limit = 100
    
    return start_phrase, word_limit

