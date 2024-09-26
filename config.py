from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.py')  # Ensure the file exists in the correct location

# Continue with your application setup...
