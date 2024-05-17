from flask import Flask, request, jsonify, render_template
import json
from VSChatbot.main import Chatbot

app = Flask(__name__)
chatbot = Chatbot()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data['message']
    language = data.get('language', 'es')  # Default to English if language is not provided

    response = chatbot.get_chatbot_response(message, language)
    return jsonify({'response': response})

@app.route('/initial_messages', methods=['POST'])
def initial_messages():
    data = request.json
    language = data.get('language', 'es')  # Default to English if language is not provided
    messages = chatbot.get_initial_messages(language)
    return jsonify({'messages': messages})

if __name__ == '__main__':
    app.run(debug=False,port=10000)
