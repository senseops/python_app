from flask import Flask, request, render_template_string
import sqlite3
import os
import subprocess
import bcrypt
from markupsafe import escape

app = Flask(__name__)

# Use environment variables for sensitive information
DB_USER = os.getenv('DB_USER', 'admin')  # Default to 'admin' if not set
DB_PASSWORD = os.getenv('DB_PASSWORD', 'secret')  # Default to 'secret' if not set

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    # Use parameterized queries to prevent SQL Injection
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return f"User: {user}"
    else:
        return "User not found", 404

@app.route('/hash', methods=['POST'])
def hash_password():
    password = request.form.get('password')
    # Use bcrypt for stronger password hashing
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return f"Hashed Password: {hashed.decode()}"  # Decoding for better readability

@app.route('/command', methods=['POST'])
def execute_command():
    command = request.form.get('command')

    # Define a whitelist of allowed commands
    allowed_commands = {
        "list_files": ["ls", "-l"],   # Example command
        "current_directory": ["pwd"],
        # Add other safe commands here
    }

    if command in allowed_commands:
        output = subprocess.run(allowed_commands[command], capture_output=True, text=True)
        return f"Command output: {output.stdout}"
    else:
        return "Invalid command", 400

@app.route('/greet', methods=['GET'])
def greet_user():
    name = request.args.get('name', '')
    # Properly escape user input to prevent XSS
    return render_template_string(f"<h1>Hello, {escape(name)}</h1>")

if __name__ == '__main__':
    app.run(debug=True)
