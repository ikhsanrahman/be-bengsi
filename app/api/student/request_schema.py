"""
	REQUEST SCHEMA
"""

from werkzeug.datastructures import FileStorage
from flask_restplus import reqparse


######################### STUDENT ####################################

class RegisterStudentRequestSchema:
	"""Define all mandatory argument for creating User"""
	parser = reqparse.RequestParser()
	parser.add_argument("full_name",    	type=str, required=True)
	parser.add_argument("email",        	type=str, required=True)
	parser.add_argument("password",   		type=str, required=True)
	parser.add_argument("phone_number",		type=str, required=True)
	parser.add_argument("gender", 			type=str, required=True)
	parser.add_argument("grade",        	type=str, required=True)
	parser.add_argument("school",   		type=str, required=True)
	parser.add_argument("address",			type=str, required=True)

#end class

class LoginStudentRequestSchema:
	parser = reqparse.RequestParser()
	parser.add_argument("email",    				type=str, required=True)
	parser.add_argument("password",        			type=str, required=True)
	parser.add_argument("confirm_password", 		type=str, required=True)

class UpdateStudentRequestSchema:
	parser = reqparse.RequestParser()
	parser.add_argument("full_name",    		type=str, required=True)
	parser.add_argument("phone_number",			type=str, required=True)
	parser.add_argument("gender", 					type=str, required=True)
	parser.add_argument("grade",    				type=str, required=True)
	parser.add_argument("school",						type=str, required=True)
	parser.add_argument("address", 					type=str, required=True)


class SearchStudentNameRequestSchema:
	parser = reqparse.RequestParser()
	parser.add_argument("name",    					type=str, required=True)

class UpdatePasswordRequestSchema:
	parser = reqparse.RequestParser()
	parser.add_argument("email", 					   					 type=str, required=True)
	parser.add_argument("new_password",                type=str, required=True)
	parser.add_argument("confirm_new_password",        type=str, required=True)

class ForgetPasswordRequestSchema:
	parser = reqparse.RequestParser()
	parser.add_argument("email", 					   						type=str, required=True)
	parser.add_argument("new_password",                	type=str, required=True)
	parser.add_argument("confirm_new_password",        	type=str, required=True)