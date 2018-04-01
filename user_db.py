import datetime
from app import DB
from flask import current_app
from sqlalchemy.dialects.postgresql import JSON
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from sqlalchemy import ForeignKey

# Represents the data base table for the users 
class User_DB(DB.Model):
    __tablename__ = 'users'

    id = DB.Column(DB.Integer, primary_key=True)
    email = DB.Column(DB.String(254))
    password_hash = DB.Column(DB.String(128))
    name = DB.Column(DB.String(32))
    surname = DB.Column(DB.String(32))
    age = DB.Column(DB.Integer)
    gender = DB.Column(DB.String(32))
    location= DB.Column(DB.String(32))
    occupation = DB.Column(DB.String(32))
    interests = DB.Column(DB.String(256))
    date_created = DB.Column(DB.DateTime, default=datetime.datetime.utcnow)
    # defaults to creation time but should be changed each time user checks in 
    lastCheckIn = DB.Column(DB.DateTime)
    # Foreign Key creates a pointer to the locations table - google location id column
    checkInLocation = DB.Column(DB.String(255), ForeignKey('locations.gid')) #user.currentLocation for actual location object
    # Foreign Key creates a pointer to the matched user
    matchedUser = DB.Column(DB.Integer, ForeignKey('users.id'))
    matchedMessage = DB.Column(DB.String(256))
    matchedTopics = DB.Column(DB.String(128))

    # result_all = DB.Column(JSON)
    # result_no_stop_words = DB.Column(JSON)

    # def __init__(self, name, surname, result_all, result_no_stop_words):
    def __init__(self, email):
        self.email = email
        # self.result_all = result_all
        # self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration = 86400):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User_DB.query.get(data['id'])
        return user