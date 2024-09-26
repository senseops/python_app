from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Create a simple SQLite database and users table
def init_db():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
    cursor.execute("INSERT INTO users (name) VALUES ('Alice')")
    cursor.execute("INSERT INTO users (name) VALUES ('Bob')")
    conn.commit()
    conn.close()

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve user information based on user ID with a vulnerable SQL query."""
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    # Vulnerable to SQL injection
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"id": user[0], "name": user[1]}), 200
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)  # Enable debug mode for testing
