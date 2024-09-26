from flask import Flask, jsonify

app = Flask(__name__)

# Vulnerable: Exposed secret (API key)
API_KEY = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"  # Example API key

@app.route('/secret', methods=['GET'])
def get_secret():
    """Endpoint that returns the exposed API key."""
    return jsonify({"api_key": API_KEY}), 200

if __name__ == '__main__':
    import os
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)  # Enable debug mode based on environment variable
