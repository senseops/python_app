from flask import Flask, request, render_template_string, jsonify
import sqlite3
import os
import subprocess
import bcrypt
from markupsafe import escape

app = Flask(__name__)

# Use environment variables for sensitive information
DB_USER = os.getenv('DB_USER', 'admin')  # Default to 'admin' if not set
DB_PASSWORD = os.getenv('DB_PASSWORD', 'secret')  # Default to 'secret' if not set
DATABASE = 'example.db'

def get_db_connection():
    """Create a new database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Enable accessing rows by column name
    return conn

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve user information based on user ID."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE id = ?"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
    except sqlite3.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        conn.close()

    if user:
        return jsonify(dict(user)), 200  # Return user as JSON
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/hash', methods=['POST'])
def hash_password():
    """Hash a password using bcrypt."""
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "Password is required"}), 400

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return jsonify({"hashed_password": hashed.decode()}), 200  # Return hashed password as JSON

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
            return jsonify({"error": "Command execution failed", "details": str(e)}), 500
    else:
        return jsonify({"error": "Invalid command"}), 400

@app.route('/greet', methods=['GET'])
def greet_user():
    """Greet the user with a personalized message."""
    name = request.args.get('name', '')
    return render_template_string(f"<h1>Hello, {escape(name)}</h1>"), 200

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production
