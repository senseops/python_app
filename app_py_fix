from flask import Flask, request, render_template_string, escape
import sqlite3
import os
import subprocess
import hashlib
from bcrypt import hashpw, gensalt

app = Flask(__name__)

# Hardcoded credentials (bad practice)
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    # SQL Injection vulnerability
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return f"User: {user}"

@app.route('/hash', methods=['POST'])
def hash_password():
    password = request.form.get('password')
    # Use bcrypt for secure password hashing
    hashed = hashpw(password.encode(), gensalt())
    return f"Bcrypt Hash: {hashed.decode()}"

ALLOWED_COMMANDS = {
    "date": ["date"],
    "uptime": ["uptime"],
    "whoami": ["whoami"]
}

@app.route('/command', methods=['POST'])
def execute_command():
    command = request.form.get('command')
    if command in ALLOWED_COMMANDS:
        output = subprocess.run(ALLOWED_COMMANDS[command], capture_output=True, text=True)
        return f"Command output: {output.stdout}"
    else:
        return "Error: Command not allowed", 400

@app.route('/greet', methods=['GET'])
def greet_user():
    name = request.args.get('name', '')
    # Cross-Site Scripting (XSS): reflecting user input without sanitization
    return render_template_string(f"<h1>Hello, {{ name }}</h1>", name=escape(name))  # Escaped to prevent XSS

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)
