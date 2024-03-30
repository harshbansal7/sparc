from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class Complaint(db.Model):
    __tablename__ = "complaint"
    id = db.Column(db.Integer, primary_key=True)
    # Complaint Data
    complaint_category = db.Column(db.String(100))
    coordinatex = db.Column(db.String(20))
    coordinatey = db.Column(db.String(20))
    original = db.Column(db.String(500))
    description = db.Column(db.String(500))
    language = db.Column(db.String(3))
    # User Data
    username = db.Column(db.String(100))
    useremail = db.Column(db.String(100))
    userphone = db.Column(db.String(12))