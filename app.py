# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
import nltk

from fanfic import generate_fanfic

nltk.download('punkt')

app = Flask(__name__)

# Enable CORS
CORS(app, resources={r"/*": {"origins": ["https://allansuresh.com"]}}, supports_credentials=True)

@app.before_first_request
def load_model():
    global markov_model
    model_path = Path(__file__).parent / "markov_model.pkl"
    if model_path.exists():
        with open(model_path, 'rb') as f:
            markov_model = pickle.load(f)
    else:
        raise FileNotFoundError("Markov model file not found. Please run `build_model.py` to generate it.")

@app.route('/generate', methods=['POST'])
def generate_story():
    if request.method == 'OPTIONS':
        return jsonify({'success': True}), 200  # Respond to the preflight request
    try:
        # Get JSON data from the POST request
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400

        # Extract parameters
        start_phrase = data.get('start', 'harry potter')
        word_limit = int(data.get('limit', 100))

        # Generate the story using the pre-loaded model
        story = generate_fanfic(start_phrase, word_limit)

        return jsonify({'success': True, 'story': story})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
