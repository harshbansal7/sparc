from collections import deque
from flask import Flask, request, jsonify
from models.models import db, Complaint
from os import environ
from helpers.message import message_helper
from helpers.twilio_client import dispatch_message_to_whatsapp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

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

@app.route('/process_incoming_message', methods=['POST'])
def process_incoming_message():
    msgBody = str(request.form.to_dict()['Body'])
    complaint_id, status, *remarks = msgBody.split(" ")

    if status.lower() == 'solved':
        complaint = db.session.get(Complaint, complaint_id)
        
        if not complaint:
            # Complaint Not Found or Key Invalid 
            return jsonify({'ERROR' : 'Complaint Not Found'})
        
        complaint.status = "SOLVED"

        dispatch_message_to_whatsapp(
            f"Your Complaint registered with ID - *{complaint_id}* alloted to *{allotment[complaint.complaint_category]['official']}* has been resolved.",
            "+91" + str(complaint.userphone)
        )

        db.session.commit()

        return jsonify("SUCCESS")
    
    return jsonify("FAILED")

@app.route('/queue_complaint', methods=['POST'])
def queue_complaint():
    complaint_data = request.json['complaint_data'] 
    user_data = request.json['user_data']

    receiver_details = allotment.get(complaint_data['complaint_category'], None)
    
    if receiver_details:

        complaint_db_entry = Complaint(
            complaint_category = complaint_data['complaint_category'],
            coordinatex = complaint_data['coordinatex'],
            coordinatey = complaint_data['coordinatey'],
            original = complaint_data['original'],
            description = complaint_data['description'],
            language = complaint_data['language'],

            username = user_data['username'],
            useremail = user_data['useremail'],
            userphone = user_data['userphone'],
            
            status = 'LODGED',
        )

        db.session.add(complaint_db_entry)

        db.session.commit()

        message = message_helper(complaint_db_entry.id, receiver_details, complaint_data, user_data=None)
                
        status = dispatch_message_to_whatsapp(message, receiver_details['contactno'])

        confirmation = dispatch_message_to_whatsapp(
            f"""Your Complaint has been received by the {receiver_details["official"]} and will be responded to very shortly.\n\nYou may use this for your reference: *Complaint ID - {complaint_db_entry.id}*\n\nYou may reply to this message to give your feedback on the service.""",
            "+91" + str(user_data['userphone'])
        )

        # message_status = "PENDING"

        # if len(MessageQueue) != 0:
        #     MessageQueue.append(packet)
        #     message_status = "QUEUED"
        # else:
        #     status = dispatch_message_to_whatsapp(packet)

        #     if not status:
        #         MessageQueue.append(packet)
        #         message_status = "QUEUED"
        #     else:
        #         message_status = status

    

    return jsonify({
        "status": status,
        "allocated_to": receiver_details['official'], 
        "message": f"Complaint has been lodged with ID - {complaint_db_entry.id}. You will be contacted soon for a follow-up."
    })

    # class Complaint(db.Model):
    #     __tablename__ = "complaint"
    #     id = db.Column(db.Integer, primary_key=True)
    #     # Complaint Data
    #     complaint_category = db.Column(db.String(100))
    #     coordinatex = db.Column(db.String(20))
    #     coordinatey = db.Column(db.String(20))
    #     original = db.Column(db.String(500))
    #     description = db.Column(db.String(500))
    #     language = db.Column(db.String(3))
    #     # User Data
    #     username = db.Column(db.String(100))
    #     useremail = db.Column(db.String(100))
    #     userphone = db.Column(db.String(12))

with app.app_context():
    db.drop_all()
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)

# Things left to add-
# 1. Status of Complaint RESOLUTION Data in the Database, how do we know if it has been resolved or not.
# 2. Queue Functionality
# 3. Better way of managing complaint delivery status...still thinking