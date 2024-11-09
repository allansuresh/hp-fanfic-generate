from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": ["https://allansuresh.com"]}})

@app.route('/generate', methods=['POST'])
def generate_story():
    try:
        # Get JSON data from the POST request
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400

        # Extract parameters
        start_phrase = data.get('start', 'harry potter')
        word_limit = int(data.get('limit', 100))

        # Generate the story directly
        story = generate_fanfic(start_phrase, word_limit)

        return jsonify({'success': True, 'story': story})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
