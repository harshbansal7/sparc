import json
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

@app.route('/incoming_message', methods=['POST'])
def incoming_message():
    response = requests.post(SERVICE_2_URL + '/process_incoming_message', data=request.form) 
    return response.json()

@app.route('/api/service1/complaint', methods=['POST'])
def service1_complaint_processing():
    data = request.form  
    response = requests.post(SERVICE_1_URL + '/process_complaint', data=data) 

    # Check for Processing Errors
    if response.status_code == 400:
        return response.json()

    queue_response = requests.post(SERVICE_2_URL + '/queue_complaint', json=response.json())
    
    return jsonify(queue_response.json()), queue_response.status_code

# @app.route('/api/service2/queue-complaint')
# def get_service2_data():
#     response = requests.get(SERVICE_2_URL + '/data')
#     return response.json()

# @app.route('/api/service3')
# def get_service3_data():
#     response = requests.get(SERVICE_3_URL + '/data')
#     return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
