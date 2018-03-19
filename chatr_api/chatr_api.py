# run: pip install -r requirements.txt to install the req's
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_restful import Resource, Api
# ^ not used currently but very useful 

from flask import Flask

APP = Flask(__name__)

@APP.route("/")
def hello():
    return "Hello, welcome to the Chatr API!"


if __name__ == '__main__':
    APP.run(debug=True)

