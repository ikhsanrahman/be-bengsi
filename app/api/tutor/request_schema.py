"""
	REQUEST SCHEMA
"""

from werkzeug.datastructures import FileStorage
from flask_restplus import reqparse


######################### TUTOR ####################################

class RegisterTutorRequestSchema:
	"""Define all mandatory argument for creating TUTOR"""
	parser = reqparse.RequestParser()
	parser.add_argument("full_name",    	type=str, required=True)
	parser.add_argument("email",        	type=str, required=True)
	parser.add_argument("password",   		type=str, required=True)
	parser.add_argument("phone_number",		type=str, required=True)
	parser.add_argument("gender", 			type=str, required=True)
	parser.add_argument("education",        	type=str, required=True)
	parser.add_argument("address",			type=str, required=True)
	parser.add_argument("experience",		type=str, required=True)

#end class

class LoginTutorRequestSchema:
	parser = reqparse.RequestParser()
	parser.add_argument("email",    				type=str, required=True)
	parser.add_argument("password",        			type=str, required=True)
	parser.add_argument("confirm_password", 		type=str, required=True)

class UpdateTutorRequestSchema:
	parser = reqparse.RequestParser()
	parser.add_argument("full_name",    		type=str, required=True)
	parser.add_argument("phone_number",			type=str, required=True)
	parser.add_argument("gender", 					type=str, required=True)
	parser.add_argument("education",    				type=str, required=True)
	parser.add_argument("address", 					type=str, required=True)
	parser.add_argument("experience", 					type=str, required=True)


class SearchTutorNameRequestSchema:
	parser = reqparse.RequestParser()
	parser.add_argument("name",    					type=str, required=True)

class TutorIsWorkingRequestSchema:
	parser = reqparse.RequestParser()
	parser.add_argument("tutoroff",    					type=bool)
	parser.add_argument("tutoron",    					type=bool)

class GetTutorRequestSchema:
	parser = reqparse.RequestParser()
	parser.add_argument("status_true",    					type=bool)
	parser.add_argument("status_false",    					type=bool)	


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


# #------------------------------- PRODUCT ------------------------------#

# class UploadProductRequestSchema:
# 	parser = reqparse.RequestParser()
# 	parser.add_argument("file_title", type=str, required=True)
# 	parser.add_argument("file_name", type=FileStorage, location='files', required=True)

# class UpdateProductRequestSchema:
# 	parser = reqparse.RequestParser()
# 	parser.add_argument("file_title", type=str, required=True)
# 	parser.add_argument("file_name", type=FileStorage, location='files', required=True)



# #------------------------------- ITEM ------------------------------#

# class UploadItemRequestSchema:
# 	parser = reqparse.RequestParser()
# 	parser.add_argument("item_title", type=str, required=True)
# 	parser.add_argument("price", 		type=str, required=True)
# 	parser.add_argument("description", type=str, required=True)

# class UpdateItemRequestSchema:
# 	parser = reqparse.RequestParser()
# 	parser.add_argument("item_title", type=str, required=True)
# 	parser.add_argument("price", 		type=str, required=True)
# 	parser.add_argument("description", type=str, required=True)

# #--------------------------------- BUYER ----------------------------------#


# class RegisterBuyerRequestSchema:
# 	"""Define all mandatory argument for creating User"""
# 	parser = reqparse.RequestParser()
# 	parser.add_argument("full_name",    type=str, required=True)
# 	parser.add_argument("email",        type=str, required=True)
# 	parser.add_argument("password",   	type=str, required=True)
# 	parser.add_argument("phone_number",	type=str, required=True)
# 	parser.add_argument("gender", 		type=str, required=True)
# 	parser.add_argument("address", 		type=str, required=True)
# #end class

# class LoginBuyerRequestSchema:
# 	parser = reqparse.RequestParser()
# 	parser.add_argument("email",    		type=str, required=True)
# 	parser.add_argument("password",        	type=str, required=True)
# 	parser.add_argument("confirm_password",        	type=str, required=True)

# class UpdateBuyerRequestSchema:
# 	parser = reqparse.RequestParser()
# 	parser.add_argument("full_name",    		type=str, required=True)
# 	parser.add_argument("phone_number",			type=str, required=True)
# 	parser.add_argument("gender", 				type=str, required=True)
# 	parser.add_argument("address", 				type=str, required=True)
	
# class SearchBuyerNameRequestSchema:
# 	parser = reqparse.RequestParser()
# 	parser.add_argument("full_name",    type=str, required=True)


# class UpdatePasswordRequestSchema:
# 	parser = reqparse.RequestParser()
# 	parser.add_argument("email", 					   type=str, required=True)
# 	parser.add_argument("new_password",                type=str, required=True)
# 	parser.add_argument("confirm_new_password",        type=str, required=True)

# class ForgetPasswordRequestSchema:
# 	parser = reqparse.RequestParser()
# 	parser.add_argument("email", 					   type=str, required=True)
# 	parser.add_argument("new_password",                type=str, required=True)
# 	parser.add_argument("confirm_new_password",        type=str, required=True)

