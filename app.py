import os
from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
import datetime


APP = Flask(__name__)
APP.config.from_object(os.environ['APP_SETTINGS'])

APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)
auth = HTTPTokenAuth(scheme='Token')

from user_db import *
from location_db import *

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
		abort(409)    # existing user
	user = User_DB(email=email)
	user.hash_password(password)
	DB.session.add(user)
	DB.session.commit()
	g.user = user
	token = g.user.generate_auth_token()
	return jsonify({ 'token': token.decode('ascii') })
	# return (jsonify({'email': user.email}), 201, {'Location': url_for('get_user', id=user.id, _external=True)})

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

	
@APP.route('/api/v1/users/<int:id>', methods=['GET'])
@auth.login_required
def get_user(id):
	if id == 0:
		user = g.user
	else:
		user = User_DB.query.get(id)
	if not user:
		abort(404)
	return jsonify(
			id=user.id,
			name=user.name,
			surname=user.surname,
			age=user.age,
			gender=user.gender,
			location=user.location,
			occupation=user.occupation,
			interests=user.interests
		)


@APP.route('/api/v1/location/<string:gid>', methods=['GET'])
@auth.login_required
def getLocation(gid):
	location = Location_DB.query.filter_by(gid=gid).first()
	if location is not None:
		return jsonify(
				id=location.id,
				gid=location.gid,
				name=location.name,
				address=location.address,
				phoneNumber=location.phoneNumber,
				priceLevel=location.priceLevel,
				rating=location.rating
			)
	else:
		abort(404)


@APP.route('/api/v1/location', methods=['POST'])
@auth.login_required
def newLocation():
	gid = request.json.get('gid')
	name = request.json.get('name')
	address = request.json.get('address')
	phoneNumber = request.json.get('phoneNumber')
	priceLevel = request.json.get('priceLevel')
	rating = request.json.get('rating')
	location = Location_DB.query.filter_by(gid=gid).first()
	if location is None:
		location = Location_DB(gid=gid, name=name, address=address, phoneNumber=phoneNumber, priceLevel=priceLevel, rating=rating)
		DB.session.add(location)
		DB.session.commit()
		return jsonify(
				id=location.id,
				gid=location.gid,
				name=location.name,
				address=location.address,
				phoneNumber=location.phoneNumber,
				priceLevel=location.priceLevel,
				rating=location.rating
			)
	else:
		abort(409)

@APP.route('/api/v1/users/profile', methods=['POST'])
@auth.login_required
def updateProfile():
	name = request.json.get('name')
	surname = request.json.get('surname')
	age = request.json.get('age')
	gender = request.json.get('gender')
	location = request.json.get('location')
	occupation = request.json.get('occupation')
	interests = request.json.get('interests')
	g.user.name = name
	g.user.surname = surname
	g.user.age = age
	g.user.gender = gender
	g.user.location = location
	g.user.occupation = occupation
	g.user.interests = interests
	DB.session.commit()
	return jsonify(
			id=g.user.id,
			email=g.user.email,
			name=g.user.name,
			surname=g.user.surname,
			age=g.user.age,
			gender=g.user.gender,
			location=g.user.location,
			occupation=g.user.occupation,
			interests=g.user.interests
		)

@APP.route('/api/v1/resource')
@auth.login_required
def get_resource():
	if g.user.name is None:
		return jsonify({'data': 'Hello, %s!' % g.user.email})
	return jsonify({'data': 'Hello, %s!' % g.user.name})

@APP.route('/api/v1/users/match', methods=['GET'])
@auth.login_required
def get_match():
	matched_id = -1
	matched_name = ""
	matched_surname = ""
	matched_user = None
	if g.user.matchedUser is not None:
		matched_id = g.user.matchedUser
		matched_user = User_DB.query.get(matched_id)
		if matched_user is not None:
			matched_name = matched_user.name
			matched_surname = matched_user.surname
	return jsonify(
		id=matched_id,
		name=matched_name,
		surname=matched_surname
	)
	# matchedUser = g.user.matchedUser
	# if matchedUser is None:
	# 	return jsonify(result=False)
	# return jsonify(
	# 		result=True,
	# 		id=matchedUser.id,
	# 		name=matchedUser.name,
	# 		surname=matchedUser.surname,
	# 	)


def get_interests(interests_str):
	interests_str = interests_str.replace(" ", "")
	curr_interest, interests = "", []
	for c in interests_str:
		if c == ",":
			interests.append(curr_interest)
			curr_interest = ""
		else: curr_interest += c
	return []


@APP.route('/api/v1/location/<string:gid>/checkin', methods=['GET'])
@auth.login_required
def user_checkin(gid):
	location = Location_DB.query.filter_by(gid=gid).first()
	if location is None:
		abort(404)
	time_now = datetime.datetime.utcnow()
	matched = None
	matched_id = -1
	matched_name = ""
	matched_surname = ""
	# g.user.lastCheckIn = datetime.datetime.utcnow
	# g.user.checkInLocation = None
	# DB.session.commit()
	print ("Before")
	print (location.checkedInUsers)
	for u in location.checkedInUsers:
		if u.lastCheckIn is not None and time_now - u.lastCheckIn > datetime.timedelta(minutes=2):
			print (time_now - u.lastCheckIn)
			u.checkInLocation = None
		elif u is not g.user and matched is None: # need to check that user is not matched
			u.matchedUser = g.user.id
			g.user.matchedUser = u.id
			matched = u
			print ("matched")
			print (matched)
			print (matched.id)
			matched_id = matched.id
			matched_name = matched.name
			matched_surname = matched.surname
	if g.user not in location.checkedInUsers:
		location.checkedInUsers.append(g.user)
	print ("After")
	print (location.checkedInUsers)
	g.user.lastCheckIn = time_now
	DB.session.commit()
	return jsonify(
		id=matched_id,
		name=matched_name,
		surname=matched_surname
	)


if __name__ == "__main__":
	APP.run() #(host='0.0.0.0', port=5000, debug=True)