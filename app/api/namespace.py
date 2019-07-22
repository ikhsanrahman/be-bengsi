from flask_restplus import Namespace, fields

class Home:
	api = Namespace('Home', description='api related to first access')

class Student :
	api = Namespace('Buyer', description='api related to Buyer')

class Tutor :
	api = Namespace('Seller', description='api related to Seller ')

class Admin:
	api = Namespace('admin', description="api for monitoring apps")

class Subject:
	api = Namespace('Subject', description='api related to Subject')

class Summary:
	api = Namespace('Summary', description="api for Summary between Student and tutor")
