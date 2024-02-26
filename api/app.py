from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Microservice endpoints
SERVICE_1_URL = "http://service1:5001"
SERVICE_2_URL = "http://service2:5002"
SERVICE_3_URL = "http://service3:5003"

# API endpoints
@app.route('/')
def normal():
    return jsonify("API is Running!")

@app.route('/api/service1', methods=['POST'])
def process_data():
    data = request.form  # Get form data
    response = requests.post(SERVICE_1_URL + '/process_input', data=data)  # Forward data to Microservice 1
    return response.json()

@app.route('/api/service2')
def get_service2_data():
    response = requests.get(SERVICE_2_URL + '/data')
    return response.json()

@app.route('/api/service3')
def get_service3_data():
    response = requests.get(SERVICE_3_URL + '/data')
    return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
