import os
from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth


APP = Flask(__name__)
APP.config.from_object(os.environ['APP_SETTINGS'])

APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)
auth = HTTPTokenAuth(scheme='Token')

from user_db import *

@APP.route("/")
def hello():
	return "<h1 style='color:blue'>Hello There!</h1>"

# @auth.verify_password
# def verify_password(email_or_token, password):
# 	# first try to authenticate by token
# 	user = User_DB.verify_auth_token(email_or_token)
# 	if not user:
# 		# try to authenticate with email/password
# 		user = User_DB.query.filter_by(email=email_or_token).first()
# 		if not user or not user.verify_password(password):
# 			return False
# 	g.user = user
# 	return True

@auth.verify_token
def verify_token(token):
	print ('verify_token')
	print (token)
	user = User_DB.verify_auth_token(token)
	if not user:
		return False
	g.user = user
	return True

@APP.route('/api/v1/token')
@auth.login_required
def get_auth_token():
	token = g.user.generate_auth_token()
	return jsonify({ 'token': token.decode('ascii') })

@APP.route('/api/v1/users/register', methods=['POST'])
def new_user():
	email = request.json.get('email')
	password = request.json.get('password')
	if email is None or password is None:
		abort(400)    # missing arguments
	if User_DB.query.filter_by(email=email).first() is not None:
		abort(400)    # existing user
	user = User_DB(email=email)
	user.hash_password(password)
	DB.session.add(user)
	DB.session.commit()
	return (jsonify({'email': user.email}), 201, {'Location': url_for('get_user', id=user.id, _external=True)})

@APP.route('/api/v1/users/login', methods=['POST'])
def login_user():
	email = request.json.get('email')
	password = request.json.get('password')
	if email is None or password is None:
		abort(400)    # missing arguments
	user = User_DB.query.filter_by(email=email).first()
	if user is None:
		abort(400)    # user doesn't exist
	if user.verify_password(password):
		g.user = user
		token = g.user.generate_auth_token()
		return jsonify({ 'token': token.decode('ascii') })
	abort(401)

	
@APP.route('/api/v1/users/<int:id>')
def get_user(id):
	user = User_DB.query.get(id)
	if not user:
		abort(400)
	return jsonify({'email': user.email})


@APP.route('/api/v1/resource')
@auth.login_required
def get_resource():
	return jsonify({'data': 'Hello, %s!' % g.user.email})

if __name__ == "__main__":
	APP.run() #(host='0.0.0.0', port=5000, debug=True)