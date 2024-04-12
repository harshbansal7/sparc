from tempfile import NamedTemporaryFile
from flask import Flask, request, jsonify
from helpers.audio_transcription import speech_to_text
from helpers.category_prediction import clean_text, complaint_category_prediction #speech to text module from MCS
from helpers.text_handling import get_complaint_language, translate_complaint
from wtforms import Form, StringField, IntegerField, DecimalField, validators

app = Flask(__name__)

class ComplaintRequest(Form):
    username = StringField('username', [validators.Length(min=4, max=25), validators.InputRequired()])
    useremail = StringField('useremail', [validators.Length(min=6, max=35), validators.InputRequired()])
    userphone = IntegerField('userphone', [validators.InputRequired()])
    complaint = StringField('complaint', [validators.InputRequired(), validators.Length(min=10, max=500)])
    latitude = DecimalField('latitude', places=2)
    longitude = DecimalField('longitude', places=2)

class User:
    def __init__(self, name, phone, email):
        self.UserName = name
        self.UserPhone = phone
        self.UserEmail = email
        
class Complaint:
    def __init__(self, user, complaint, x, y, audio_file=None):
        """
        Initialize a Complaint object with user, complaint description, coordinates, and optional audio file.

        Parameters:
        - user: User object representing the complainant
        - complaint: Original complaint description
        - x: X-coordinate of the location associated with the complaint
        - y: Y-coordinate of the location associated with the complaint
        - audio_file: Optional audio file containing additional details about the complaint
        """
        self.User = user  # Assigning a User object
        self.OriginalComplaint = complaint

        # Determine the language of the complaint and translate if necessary
        self.Language = get_complaint_language(complaint)
        if self.Language != 'en':
            self.Description = translate_complaint(
                input=self.OriginalComplaint,
                fromlang=self.Language
            )
        else:
            self.Description = complaint

        # self.description is the final usable complaint (in english)
        self.latitude = x
        self.longitude = y
        self.AudioFile = audio_file

        self.ComplaintCategory = None

    def setPredictedCategory(self, predictedCategory):
        self.ComplaintCategory = predictedCategory
        return True

    def getDictionary(self, includeUserData=True):
        local_dict = {
            'complaint_data' : {
                'original': self.OriginalComplaint,
                'language': self.Language,
                'description': self.Description,
                'latitude': self.latitude,
                'longitude': self.longitude,
                'complaint_category': self.ComplaintCategory,
            }
        }

        if includeUserData:
            local_dict['user_data'] = {
                'username':self.User.UserName,
                'useremail':self.User.UserEmail,
                'userphone':self.User.UserPhone,
            }
        
        return jsonify(local_dict)

@app.route('/process_complaint', methods=['POST'])
def process_complaint():
    form = ComplaintRequest(request.form)
    
    # Check Request Data Validation
    if not form.validate():
        errors = form.errors
        return jsonify({"errors": errors}), 400

    if 'audiofile' in request.files:
        audiofile = request.files['audiofile']
        with NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_path = temp_audio_file.name
            temp_audio_file.write(audiofile.file.read())
            audio_text = speech_to_text(temp_audio_path)

        return jsonify("If you have reached here, you're probably sitting right next to the Developer!😉 Sorry but we are still working on Audio Processing!")
    else:
        complaint_object = Complaint(
            user = User(form.username.data, form.userphone.data, form.useremail.data),
            complaint= form.complaint.data,
            x = form.latitude.data,
            y = form.longitude.data,
        )

        processed_complaintText = clean_text(complaint_object.Description)
        
        if not processed_complaintText:
            return jsonify({"errors": ['The input complaint text after translation (if applicable) is not suitable for prediction.']}), 400

        ComplaintCategory = complaint_category_prediction(processed_complaintText)
        complaint_object.setPredictedCategory(ComplaintCategory)
            
        return complaint_object.getDictionary()
    
        # SAMPLE OUTPUT
        # {
        #     "complaint_data": {
        #         "complaint_category": "ASSAULT AND THREAT",
        #         "coordinatex": "10.550",
        #         "coordinatey": "20.2003",
        #         "description": "The accused allegedly assaulted the complainant with a wooden stick and threatened to kill him.",
        #         "language": "en",
        #         "original": "The accused allegedly assaulted the complainant with a wooden stick and threatened to kill him."
        #     },
        #     "user_data": {
        #         "useremail": "harsh@gmail.com",
        #         "username": "Harsh",
        #         "userphone": 1000101
        #     }
        # }
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
