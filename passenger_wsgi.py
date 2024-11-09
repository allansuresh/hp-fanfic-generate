import os
import sys
from app import app  # Import the Flask app directly

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set the application variable to your Flask app
application = app
