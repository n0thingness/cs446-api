import datetime
from app import DB
from flask import current_app
from sqlalchemy.dialects.postgresql import JSON
# from passlib.apps import custom_app_context as pwd_context
# from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

# Represents the data base table for the locations and related data 
class Location_DB(DB.Model):
    __tablename__ = 'locations'

    id = DB.Column(DB.Integer, primary_key=True)
    gid = DB.Column(DB.String(255)) # google id, api returns location with id 
    name = DB.Column(DB.String(127))
    address = DB.Column(DB.String(127))
    phoneNumber = DB.Column(DB.String(50))
    priceLevel = DB.Column(DB.Integer)
    rating = DB.Column(DB.Float)

    currentUserCount = DB.Column(DB.Integer) 
    userList = [] # list to track the number of users at the location

    def __init__(self, gid, name=None, address=None, phoneNumber=None, priceLevel=0, rating=0):
        self.gid = gid 
        self.name = name
        self.address = address
        self.phoneNumber = phoneNumber
        self.priceLevel = priceLevel
        self.rating = rating
        self.currentUserCount = 0

    def __repr__(self):
        return '<location id {}>'.format(self.id)

    # def add_user_to_location(self, user_id):
    #     self._current_user_count += 1 # increment user count at location 
    #     self._users_list.append(user_id) # add user id to l of users at location

    # def remove_user_from_location(self, user_id):
    #     self._current_user_count -= 1
    #     self._users_list.remove(user_id)

    # def get_users_at_location_count(self, location_id):
    #     userc = Location_DB.session.query(location_id).get(_current_user_count)
    #     return userc

    # def get_all_users_at_location(self, location_id):
    #     userl = Location_DB.session.query(location_id).get(_users_list)
    #     return userl

    # def get_all_unmatched_users_at_location(self, location_id):
    #     all_users = Location_DB.session.query(location_id).get(_users_list)
    #     matched_users = User_DB.query.filter_by(is_matched=True).get()
    #     return list(set(all_users) - set(matched_users)) 

