from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/queue_complaint', methods=['POST'])
def queue_complaint():
    return jsonify({"message": "Data from Microservice 2"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
