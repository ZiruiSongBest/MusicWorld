import os
from flask import Flask, request, jsonify
from flask_cors import CORS # type: ignore
import json

app = Flask(__name__)
CORS(app)  

from request_text_emotion import request_text_emotion # type: ignore

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        'message': 'Hello from Flask!',
        'status': 'success'
    }
    return jsonify(data)

@app.route('/api/post', methods=['POST'])
def post_data():
    received_data = request.get_json()
    return jsonify({'message': 'Data received', 'data': received_data})

@app.route('/api/emotion', methods=['POST'])
def emotion_analysis():
    data = request.get_json()  
    text = data.get('text') 

    if text:
        try:
            emotion_result = request_text_emotion(text)
            return jsonify({'status': 'success', 'result': emotion_result}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    else:
        return jsonify({'status': 'error', 'message': 'No text provided'}), 400

@app.route('/api/get_processed_data', methods=['GET'])
def get_processed_data():
    processed_data = {
        'data': [1, 2, 3, 4, 5],
        'description': 'This is some processed data.'
    }
    return jsonify({'status': 'success', 'data': processed_data}), 200

@app.route('/api/summarize', methods=['POST'])
def summarize_text():
    data = request.get_json()
    text = data.get('text')
    if text:
        summary = text[:100] + '...'
        return jsonify({'status': 'success', 'summary': summary}), 200
    else:
        return jsonify({'status': 'error', 'message': 'No text provided'}), 400

emotion_history = []

@app.route('/api/emotion', methods=['POST'])
def emotion_analysis():
    data = request.get_json()
    text = data.get('text')
    if text:
        try:
            result = {'emotion': 'happy', 'text': text}
            emotion_history.append(result)
            return jsonify({'status': 'success', 'result': result}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    else:
        return jsonify({'status': 'error', 'message': 'No text provided'}), 400

@app.route('/api/emotion_history', methods=['GET'])
def get_emotion_history():
    return jsonify({'status': 'success', 'history': emotion_history}), 200


users = {}

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username in users:
        return jsonify({'status': 'error', 'message': 'User already exists'}), 400
    users[username] = password
    return jsonify({'status': 'success', 'message': 'User registered successfully'}), 200

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if users.get(username) == password:
        return jsonify({'status': 'success', 'message': 'Login successful'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401

@app.route('/api/user_info', methods=['POST'])
def get_user_info():
    data = request.get_json()
    username = data.get('username')
    if username in users:
        return jsonify({'status': 'success', 'user': {'username': username}}), 200
    else:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
@app.route('/api/audio_emotion', methods=['POST'])
def audio_emotion_analysis():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No file selected'}), 400
    if file:

        filename = file.filename
        file_path = os.path.join(UPLOAD, filename) # type: ignore
        file.save(file_path)

        result = {'emotion': 'calm', 'filename': filename}
        return jsonify({'status': 'success', 'result': result}), 200

if __name__ == '__main__':
    app.run(debug=True)
