from collections import deque
from flask import Flask, request, jsonify

from helpers.message import message_helper
from helpers.twilio_client import dispatch_message_to_whatsapp

app = Flask(__name__)

MessageQueue = deque()

contact_info = {
    'S.P. CRIME' : '+918146919769',
    'S.P. CYBER CRIME' : '+918146919769',
    'S.P. CRIME (JUVENILE)': '+918146919769',
    'S.P. TRAFFIC': '+918146919769',
    'CONTROL ROOM' : '+918146919769',
    'S.P. VIGILANCE' : '+918146919769',
    'S.P. EOW' : '+918146919769s',
}

allotment = {
    "ASSAULT AND THREAT": {
        'official': "S.P. CRIME",
        'contactno': contact_info['S.P. CRIME']
    },
    "CHILD OFFENDER": {
        'official': "S.P. CRIME (JUVENILE)",
        'contactno': contact_info['S.P. CRIME (JUVENILE)']
    },
    "FRAUD AND CHEATING (NON-CYBER)": {
        'official': "S.P. EOW",
        'contactno': contact_info['S.P. EOW']
    },
    "ILLEGAL ACTIVITIES": {
        'official': "S.P. VIGILANCE",
        'contactno': contact_info['S.P. VIGILANCE']
    },
    "ONLINE FRAUD": {
        'official': "S.P. CYBER CRIME",
        'contactno': contact_info['S.P. CYBER CRIME']
    },
    "PRIVACY BREACH": {
        'official': "S.P. CYBER CRIME",
        'contactno': contact_info['S.P. CYBER CRIME']
    },
    "THEFT AND ROBBERY": {
        'official': "CONTROL ROOM",
        'contactno': contact_info['CONTROL ROOM']
    },
    "TRAFFIC ACCIDENTS AND VIOLATIONS": {
        'official': "S.P. TRAFFIC",
        'contactno': contact_info['S.P. TRAFFIC']
    },
}

@app.route('/queue_complaint', methods=['POST'])
def queue_complaint():
    complaint_data = request.json['complaint_data'] 
    user_data = request.json['user_data']

    receiver_details = allotment.get(complaint_data['complaint_category'], None)

    if receiver_details:
        message = message_helper(receiver_details, complaint_data, user_data=None)
        
        packet = [message, receiver_details['contactno']]
        
        message_status = "PENDING"

        if len(MessageQueue) != 0:
            MessageQueue.append(packet)
            message_status = "QUEUED"
        else:
            status = dispatch_message_to_whatsapp(packet)

            if not status:
                MessageQueue.append(packet)
                message_status = "QUEUED"

            else:
                message_status = "SENT"

    return jsonify({"message": message_status})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
