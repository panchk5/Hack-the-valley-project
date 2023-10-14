from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from analysis import chat
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/chat', methods=['POST'])
def chat():
    return chat()

if __name__ == '__main__':
    app.run()
