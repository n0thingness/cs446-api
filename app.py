from flask import Flask
APP = Flask(__name__)

@APP.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
	# APP.run(debug=True)
    APP.run() #host='0.0.0.0'