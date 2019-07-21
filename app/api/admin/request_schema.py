from flask_restplus import reqparse

# ------------------------------ ADMIN ------------------------------------#

class AdminRequestSchema:
	parser = reqparse.RequestParser()
	parser.add_argument("name", type=str, required=True)
	parser.add_argument("password", type=str, required=True)
