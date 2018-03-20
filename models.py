import datetime
from app import db
from flask import current_app
from sqlalchemy.dialects.postgresql import JSON
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254))
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(32))
    surname = db.Column(db.String(32))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # result_all = db.Column(JSON)
    # result_no_stop_words = db.Column(JSON)

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

    def generate_auth_token(self, expiration = 600):
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
        user = User.query.get(data['id'])
        return user