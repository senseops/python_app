from flask import Flask, request, render_template_string
import sqlite3
import os
import subprocess
import hashlib

app = Flask(__name__)

# Hardcoded credentials (bad practice)
DB_USER = 'admin'
DB_PASSWORD = 'secret'

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    # SQL Injection vulnerability
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    conn.close()
    return f"User: {user}"

@app.route('/hash', methods=['POST'])
def hash_password():
    password = request.form.get('password')
    # Insecure hashing: using SHA-1 which is vulnerable to attacks
    hashed = hashlib.sha1(password.encode()).hexdigest()
    return f"SHA-1 Hash: {hashed}"

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
    return render_template_string(f"<h1>Hello, {name}</h1>")  # Vulnerable to XSS

if __name__ == '__main__':
    app.run(debug=True)
