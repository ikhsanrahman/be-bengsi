"""
	REQUEST SCHEMA
"""

from werkzeug.datastructures import FileStorage
from flask_restplus import reqparse


######################### STUDENT ####################################

class RegisterSummaryRequestSchema:
	"""Define all mandatory argument for creating User"""
	parser = reqparse.RequestParser()
	parser.add_argument("topic",    					type=str, required=True)
	parser.add_argument("date",        				type=str, required=True)
	parser.add_argument("time_started",   		type=str, required=True)
	parser.add_argument("time_ended",        	type=str, required=True)
	parser.add_argument("remarks",   					type=str, required=True)
	parser.add_argument("student_uuid",   		type=str)
	parser.add_argument("subject_uuid",      	type=str)
	parser.add_argument("summary_uuid",				type=str)
	

class UpdateSummaryRequestSchema:
	parser = reqparse.RequestParser()
	parser.add_argument("topic",    					type=str, required=True)
	parser.add_argument("date",        				type=str, required=True)
	parser.add_argument("time_started",   		type=str, required=True)
	parser.add_argument("time_ended",        	type=str, required=True)
	parser.add_argument("remarks",   					type=str, required=True)
	parser.add_argument("student_uuid",   		type=str)
	parser.add_argument("subject_uuid",      	type=str)
	parser.add_argument("summary_uuid",				type=str)

class GetSummariesRequestSchema:	
	parser = reqparse.RequestParser()
	parser.add_argument("student_uuid",    					type=str)
	parser.add_argument("tutor_uuid",        				type=str)
	parser.add_argument("subject_uuid",        				type=str)
	parser.add_argument("summary_uuid",        				type=str)
	parser.add_argument("subject_name",        				type=str)



