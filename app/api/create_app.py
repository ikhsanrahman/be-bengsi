''' 
	this module to create application from create function 
'''

import os

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS

db = SQLAlchemy()

from app.api.config.config import config_by_name


def page_not_found(e):
	error = jsonify({
			"error" 		: "Ooooopppp, where are you going ?, You are in wrong page",
			"description"	: "please check in right spelling of URL that you want to dive "
	})
	return error, 404

def run_app(config_name) :
	app = Flask(__name__)
	app.register_error_handler(404, page_not_found)
	app.config.from_object(config_by_name[config_name])
	CORS(app)
	db.init_app(app)
	app.app_context().push()
	return app