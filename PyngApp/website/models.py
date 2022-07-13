from email.policy import default
from pickle import TRUE
from . import db #from package, import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    #General schema for Notes
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(
        db.DateTime(timezone=True), 
        default=func.now()
    )

    #establishing foreign-key relationship to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #referencing database

class User(db.Model, UserMixin):
    #defining schema and layout
    id = db.Column(db.Integer, primary_key=True) #id is a primary key
    email = db.Column(db.String(150), unique=True) #email is a unique id
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    #establish the foreign-key relationship to the Notes table
    notes = db.relationship('Note') #referencing classes
