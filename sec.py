import os
from flask import Flask, jsonify

app = Flask(__name__)

# Secure: Use environment variable for the API key
API_KEY = os.getenv('API_KEY')  # Fetch from environment variable

@app.route('/secret', methods=['GET'])
def get_secret():
    """Endpoint that returns the API key if it's set."""
    if API_KEY is None:
        return jsonify({"error": "API key not configured"}), 500
    return jsonify({"api_key": API_KEY}), 200

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)  # Enable debug mode based on environment variable
