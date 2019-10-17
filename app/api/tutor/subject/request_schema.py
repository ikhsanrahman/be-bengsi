"""
	REQUEST SCHEMA
"""

from werkzeug.datastructures import FileStorage
from flask_restplus import reqparse


######################### STUDENT ####################################

class RegisterSubjectRequestSchema:
	"""Define all mandatory argument for creating User"""
	parser = reqparse.RequestParser()
	parser.add_argument("subject_name",    	type=str, required=True)
	parser.add_argument("price",        	type=str, required=True)
	parser.add_argument("description",   		type=str, required=True)

class UpdateSubjectRequestSchema:
	parser = reqparse.RequestParser()
	parser.add_argument("subject_name",    	type=str, required=True)
	parser.add_argument("price",        	type=str, required=True)
	parser.add_argument("description",   		type=str, required=True)

class SearchSubjectNameRequestSchema:
	parser = reqparse.RequestParser()
	parser.add_argument("name",    					type=str, required=True)
