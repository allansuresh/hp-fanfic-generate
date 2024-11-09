from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": ["https://allansuresh.com"]}})

@app.route('/generate', methods=['POST'])
def generate_story():
    try:
        # Get JSON data from the POST request
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400

        # Convert the JSON data to a string argument for the Python script
        input_json = json.dumps(data)

        # Construct the command to run fanfic.py with JSON input
        command = ['python3', 'fanfic.py', input_json]

        # Run the Python script and capture the output
        result = subprocess.run(command, capture_output=True, text=True)

        # Check for errors in script execution
        if result.returncode != 0:
            return jsonify({'success': False, 'error': result.stderr}), 500

        # Parse the output JSON from the script
        output = json.loads(result.stdout)

        return jsonify({'success': True, 'story': output['story'], 'parameters': output['parameters']})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
