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

    def remove_user_from_location(self, user_id):
        self._current_user_count -= 1
        self._users_list.remove(user_id)

    def get_users_at_location_count(self, location_id):
        userc = Location_DB.session.query(location_id).get(_current_user_count)
        return userc

    def get_all_users_at_location(self, location_id):
        userl = Location_DB.session.query(location_id).get(_users_list)
        return userl

    # def get_all_unmatched_users_at_location(self, location_id):
    #     all_users = Location_DB.session.query(location_id).get(_users_list)
    #     matched_users = User_DB.query.filter_by(is_matched=True).get()
    #     return list(set(all_users) - set(matched_users)) 

