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
    query = f"SELECT * FROM users WHERE id = '{user_id}'"  # Vulnerable to SQL Injection
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return f"User: {user}"

@app.route('/hash', methods=['POST'])
def hash_password():
    password = request.form.get('password')
    # Insecure hashing: using SHA-1 which is vulnerable to attacks
    hashed = hashlib.sha1(password.encode()).hexdigest()
    return f"SHA-1 Hash: {hashed}"

@app.route('/command', methods=['POST'])
def execute_command():
    command = request.form.get('command')
    # Command injection vulnerability
    output = subprocess.run(command, shell=True, capture_output=True, text=True)
    return f"Command output: {output.stdout}"

@app.route('/greet', methods=['GET'])
def greet_user():
    name = request.args.get('name', '')
    # Cross-Site Scripting (XSS): reflecting user input without sanitization
    return render_template_string(f"<h1>Hello, {name}</h1>")  # Vulnerable to XSS

if __name__ == '__main__':
    app.run(debug=True)
