import logging
from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

# Set up basic logging
logging.basicConfig(level=logging.INFO)

@app.route('/command', methods=['POST'])
def execute_command():
    """Execute a safe command based on user input."""
    command = request.form.get('command')
    
    # Define a whitelist of allowed commands
    allowed_commands = {
        "list_files": ["ls", "-l"],   # Example command
        "current_directory": ["pwd"],
        # Add other safe commands here
    }

    if command in allowed_commands:
        try:
            output = subprocess.run(allowed_commands[command], capture_output=True, text=True, check=True)
            return jsonify({"output": output.stdout}), 200
        except subprocess.CalledProcessError as e:
            # Log the error details for internal tracking
            app.logger.error(f"Command execution failed: {e}")  # Log the exception message
            return jsonify({"error": "Command execution failed"}), 500  # Generic error message
    else:
        return jsonify({"error": "Invalid command"}), 400

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production
