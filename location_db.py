import datetime
from app import DB
from flask import current_app
from sqlalchemy.dialects.postgresql import JSON
# from passlib.apps import custom_app_context as pwd_context
# from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

# Represents the data base table for the locations and related data 
class Location_DB(DB.Model):
    __tablename__ = 'locations'

    _location_id = DB.Column(DB.Integer, primary_key=True) # google id, api returns location with id 
    _name = DB.Column(DB.String(32))
    _address = DB.Column(DB.String(32))
    _current_user_count = DB.Column(DB.Integer) 
    _users_list = [] # list to track the number of users at the location

    # def __init__(self, name, surname, result_all, result_no_stop_words):
    def __init__(self, location_id, name=None, address=None):
        self._location_id = location_id 
        self._name = name
        self.address = address
        self._current_user_count = 0

    def __repr__(self):
        return '<location id {}>'.format(self._location_id)

    def add_user_to_location(self, user_id):
        self._current_user_count += 1 # increment user count at location 
        self._users_list.append(user_id) # add user id to l of users at location


    # def hash_password(self, password):
    #     self.password_hash = pwd_context.encrypt(password)

    # def verify_password(self, password):
    #     return pwd_context.verify(password, self.password_hash)

    # def generate_auth_token(self, expiration = 600):
    #     s = Serializer(current_app.config['SECRET_KEY'], expires_in = expiration)
    #     return s.dumps({ 'id': self.id })

    # @staticmethod
    # def verify_auth_token(token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token)
    #     except SignatureExpired:
    #         return None    # valid token, but expired
    #     except BadSignature:
    #         return None    # invalid token
    #     user = User.query.get(data['id'])
    #     return user