import os
from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

from models import *

@app.route("/")
def hello():
	return "<h1 style='color:blue'>Hello There!</h1>"

@auth.verify_password
def verify_password(email_or_token, password):
	# first try to authenticate by token
	user = User.verify_auth_token(email_or_token)
	if not user:
		# try to authenticate with email/password
		user = User.query.filter_by(email=email_or_token).first()
		if not user or not user.verify_password(password):
			return False
	g.user = user
	return True

@app.route('/api/v1/token')
@auth.login_required
def get_auth_token():
	token = g.user.generate_auth_token()
	return jsonify({ 'token': token.decode('ascii') })

@app.route('/api/v1/users/register', methods=['POST'])
def new_user():
	email = request.json.get('email')
	password = request.json.get('password')
	if email is None or password is None:
		abort(400)    # missing arguments
	if User.query.filter_by(email=email).first() is not None:
		abort(400)    # existing user
	user = User(email=email)
	user.hash_password(password)
	db.session.add(user)
	db.session.commit()
	return (jsonify({'email': user.email}), 201, {'Location': url_for('get_user', id=user.id, _external=True)})

@app.route('/api/v1/users/login', methods=['POST'])
def login_user():
	email = request.json.get('email')
	password = request.json.get('password')
	if email is None or password is None:
		abort(400)    # missing arguments
	user = User.query.filter_by(email=email).first()
	if user is None:
		abort(400)    # user doesn't exist
	if user.verify_password(password):
		g.user = user
		token = g.user.generate_auth_token()
		return jsonify({ 'token': token.decode('ascii') })
	abort(401)

	


@app.route('/api/v1/users/<int:id>')
def get_user(id):
	user = User.query.get(id)
	if not user:
		abort(400)
	return jsonify({'email': user.email})


@app.route('/api/v1/resource')
@auth.login_required
def get_resource():
	return jsonify({'data': 'Hello, %s!' % g.user.email})

if __name__ == "__main__":
	# app.run(debug=True)
	app.run() #host='0.0.0.0'