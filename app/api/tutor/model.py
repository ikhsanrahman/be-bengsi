from app.api.create_app import db 
from app.api.db_model import *
from app.api.tutor.serializer import TutorSchema
from .subject.serializer import SubjectSchema
from app.api.error import error
from flask import jsonify

from app.api.config.config import Config

TIME = Config.time()
err = error.Error

class TutorProcess:

	def showTutor(self):
		responses = {}
		responses['records'] = []
		contain = {}
		contain['subject'] = []
		value = {}
		tutors = Tutor.query.filter_by(activation=True, is_working=True).all()
		
		for tutor in tutors:
			contain['tutor'] = tutor.full_name
			if len(tutor.subject) > 0:
				result = SubjectSchema(many=True).dump(tutor.subject)
				for subject in result:
					contain['subject'].append(subject)

			if len(tutor.subject) == 0:
					contain['subject'] = []
			
			responses['records'].append(contain)

		return responses

	def getTutors(self, payload):

		#only display tutor with status activation true
		if payload['status_true']:
			tutors = Tutor.query.filter_by(activation=True, is_working=True).all()
			result = TutorSchema(many=True).dump(tutors)
			if tutors :
				return jsonify(result)

			if not tutors:
				return err.requestFailed("no tutor available")

		#only display tutor with status activation true
		if payload['status_false']:
			tutors = Tutor.query.filter_by(activation=False, is_working=True).all()
			result = TutorSchema(many=True).dump(tutors)
			if tutors :
				return jsonify(result)

			if not tutors:
				return err.requestFailed("no tutor available")

		#display all tutor
		if not payload['status_false'] and not payload['status_true']:
			tutors = Tutor.query.filter_by(is_working=True).all()
			result = TutorSchema(many=True).dump(tutors)
			if tutors :
				return jsonify(result)

			if not tutors:
				return err.requestFailed("no tutor available")

	def createTutor(self, payload):
		responses = {}
		get_tutor = Tutor.query.filter_by(email=payload['email']).first()

		if not get_tutor:
			new_tutor = Tutor(full_name = payload['full_name'], email=payload['email'], \
				password=payload['password'], gender=payload['gender'], education=payload['education'], \
				phone_number=payload['phone_number'], address=payload['address'] )
			new_tutor.generate_password_hash(payload['password'])
			new_tutor.created_at = TIME
			new_tutor.is_working = True
			db.session.add(new_tutor)
			db.session.commit()
			return err.requestSuccess("register new tutor success")
		
		if get_tutor :
			return err.requestFailed("tutor with that email already existed")

	def updateTutor(self, payload, tutor_uuid):
		get_tutor = Tutor.query.filter_by(tutor_uuid=tutor_uuid, status_login=True, is_working=True, activation=True).first()

		if get_tutor :
			get_tutor.full_name = payload['full_name']
			get_tutor.phone_number = payload ['phone_number']
			get_tutor.address	= payload['address']
			get_tutor.gender	= payload['gender']
			get_tutor.school	= payload['education']
			get_tutor.updated_at = TIME
			db.session.commit()
			return err.requestSuccess("update profil success")

		if not get_tutor:
			return err.badRequest("not available tutor")

	def removeTutor(self, tutor_uuid):
		get_tutor = Tutor.query.filter_by(tutor_uuid=tutor_uuid).first()

		if get_tutor :
			db.session.delete(get_tutor)
			db.session.commit()
			return err.requestSuccess("remove tutor has succeed")
		if not get_tutor:
			return err.requestFailed("no tutor available")

	def updatePassword(self, payload, tutor_uuid):
		get_tutor = Tutor.query.filter_by(tutor_uuid=tutor_uuid, email=payload['email'], status_login=True, is_working=True, activation=True).first()

		if get_tutor:
			get_tutor.password = payload['new_password']
			get_tutor.generate_password_hash(payload['new_password'])
			get_tutor.updated_at = TIME
			db.session.commit()
			return err.requestSuccess("edit password success")

		if not get_tutor:
			return err.requestFailed("tutor is not available")

	def forgetPassword(self, payload):
		get_tutor = Tutor.query.filter_by(email=payload['email'], is_working=True, activation=True).first()

		if get_tutor:
			get_tutor.password = payload['new_password']
			get_tutor.generate_password_hash(payload['new_password'])
			get_tutor.updated_at = TIME
			db.session.commit()
			return err.requestSuccess("edit forget password success")

		if not get_tutor:
			return err.requestFailed("tutor is not available")

	def loginTutor(self, payload):
		get_tutor = Tutor.query.filter_by(email=payload['email'], status_login=False, is_working=True, activation=True).first()
		
		if get_tutor and get_tutor.check_password_hash(payload['password']):
			get_tutor.time_login = TIME
			get_tutor.status_login = True
			db.session.commit()
			result = TutorSchema().dump(get_tutor)
			return jsonify(result)

		return err.requestFailed("login failed")

	def statusWorking(self, payload, tutor_uuid):
		get_tutor = Tutor.query.filter_by(tutor_uuid=tutor_uuid, status_login=True, activation=True).first()

		if get_tutor:
			if payload['tutoron']:
				get_tutor.time_tutor_on = TIME
				get_tutor.is_working = True
				db.session.commit()
				return err.requestSuccess("making tutor is working on success")
			if payload['tutoroff']:
				get_tutor.time_tutor_off = TIME
				get_tutor.is_working = False
				db.session.commit()
				return err.requestSuccess("making tutor is working off success")

		return err.requestFailed("unable making tutor is working on or off")

	def logoutTutor(self, tutor_uuid):
		get_tutor = Tutor.query.filter_by(tutor_uuid=tutor_uuid, status_login=True, is_working=True).first()

		if get_tutor:
			get_tutor.time_logout = TIME
			get_tutor.status_login = False
			db.session.commit()
			return err.requestSuccess('logout success')

		return err.requestFailed("logout failed")

	def unactivateTutor(self, tutor_uuid):
		get_tutor = Tutor.query.filter_by(tutor_uuid=tutor_uuid, activation=True).first()
		if get_tutor :
			get_tutor.activation = False
			get_tutor.is_working = False
			get_tutor.status_login = False
			get_tutor.time_tutor_off = TIME
			get_tutor.time_unactivated = TIME 
			db.session.commit()
			return err.requestSuccess("unactivate tutor success")
		if not get_tutor :
			return err.requestFailed("no tutor can be unactivated")

	def reactivateTutor(self, tutor_uuid):
		get_tutor = Tutor.query.filter_by(tutor_uuid=tutor_uuid, activation=False).first()
		if get_tutor :
			if get_tutor.activation == True:
				return err.requestFailed("tutor already active")
			else:
				get_tutor.activation = True
				get_tutor.is_working = True
				get_tutor.status_login = False
				get_tutor.time_tutor_on = TIME
				get_tutor.time_reactivated = TIME
				db.session.commit()
				return err.requestSuccess("reactivate tutor has succeed")
		
		if not get_tutor:
			return err.badRequest("tutor is not available")

	def searchTutorByName(self, payload):
		tutors = Tutor.query.filter_by(is_working=True, activation=True).all()
		result = []
		for tutor in tutors :
			if payload['name'] in tutor.full_name :
				get_tutor = TutorSchema().dump(tutor)
				result.append(get_tutor)
		if result:
			return result

		return err.badRequest("No tutor detected")
