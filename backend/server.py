from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/chat', methods=['POST'])
def chat():
    user=request.form['user']
    bot_response = "Hello, World!"
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
