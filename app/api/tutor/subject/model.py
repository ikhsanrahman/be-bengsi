from app.api.create_app import db 
from app.api.db_model import *
from app.api.tutor.subject.serializer import SubjectSchema
from app.api.error import error
from flask import jsonify

from app.api.config.config import Config

TIME = Config.time()
err = error.Error

class SubjectProcess:

	def getSubjects(self):
		subjects = Subject.query.filter_by(status=True).all()
		if subjects :
			result = SubjectSchema(many=True).dump(subjects)
			return jsonify(result)

		if not subjects:
			return err.requestFailed("no subjects available")

	def createSubject(self, payload, tutor_uuid):
		get_tutor = Tutor.query.filter_by(tutor_uuid=tutor_uuid, status_login=True,is_working=True, \
			activation=True).first()
		get_subject = Subject.query.filter_by(subject_name=payload['subject_name']).first()
		
		if get_tutor:
			if not get_subject:
				new_subject = Subject(subject_name=payload['subject_name'], price=payload['price'], \
					description=payload['description'], owner=get_tutor)
				new_subject.created_at = TIME
				db.session.add(new_subject)
				db.session.commit()
				return err.requestSuccess("register subject success")
			else:
				return err.requestFailed("the subject already existed")
		
		if not get_tutor:
			return err.requestFailed("tutor not found")

	def updateSubject(self, payload, tutor_uuid, subject_uuid):
		get_tutor = Tutor.query.filter_by(tutor_uuid=tutor_uuid, status_login=True, is_working=True, \
			activation=True).first()
		get_subject = Subject.query.filter_by(subject_uuid=subject_uuid, status=True).first()

		if get_tutor:
			if get_subject:
				get_subject.subject_name=payload['subject_name']
				get_subject.price = payload ['price']
				get_subject.description	= payload['description']
				get_subject.updated_at = TIME
				db.session.commit()
				return err.requestSuccess("update Subject success")
			if not get_subject:
				return err.requestFailed("that subject not existed")

		if not get_tutor:
			return err.badRequest("can not update")

	def unactivateSubject(self, subject_uuid):
		get_subject = Subject.query.filter_by(subject_uuid=subject_uuid, status=True).first()
		if get_subject :
			get_subject.status = False
			db.session.commit()
			return err.requestSuccess("unactivate subject success")
		if not get_subject :
			return err.requestFailed("no subject can be unactivated")

	def reactivateSubject(self, subject_uuid):
		get_subject = Subject.query.filter_by(subject_uuid=subject_uuid, status=False).first()
		if get_subject :
			if get_subject.status == True:
				return err.requestFailed("subject already active")
			else:
				get_subject.status = True
				db.session.commit()
				return err.requestSuccess("reactivate subject has succeed")
		
		if not get_subject:
			return err.badRequest("subject is not available")

	def searchSubjectByName(self, payload):
		subjects = Subject.query.all()
		result = []
		for subject in subjects :
			if payload['name'] in subject.name_subject:
				get_subjects = SubjectSchema().dump(subject)
				result.append(get_subjects)
		if result:
			return result

		return err.badRequest("No subject detected")
