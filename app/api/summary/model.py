from app.api.create_app import db 
from app.api.db_model import *
from app.api.student.serializer import StudentSchema
from app.api.error import error
from flask import jsonify

from app.api.config.config import Config

TIME = Config.time()
err = error.Error

class SummaryProcess:

	def getSummaries(self, payload):
		if payload['student_uuid']:
			result = []
			data = {}
			student = Student.query.filter_by(student_uuid=payload['student_uuid']).first()
			if student:
				for subject in student.subscriptions:
					data['subject'] = subject.name_subject
					data['name_tutor'] = subject.owner.full_name
					data['tutor_handphone'] = subject.owner.phone_number
					result.append(dict(data))
			return result

		if payload['tutor_uuid']:
			# subject, nama_student, kelas, sekolah, alamat
			result = []
			data = {}
			data['student'] = []
			contain = {}
			tutor = Tutor.query.filter_by(tutor_uuid=payload['tutor_uuid'], is_working=True, activation=True).first()
			for subject in tutor.subject:
				data['subject'] = subject.name_subject
				for student in subject.subscriber:
					contain['name_student'] = student.name_student
					contain['grade'] = student.grade
					contain['school'] = student.school
					contain['address'] =  student.address
					contain['phone_number'] = student.phone_number
					data['student'].append(dict(contain))
				result.append(data)
			return result

	def signSummary(self, payload):
		subject = Subject.query.filter_by(name_subject=payload['name_subject'], status=True).first()

		if payload['student_uuid']:
			student = Student.query.filter_by(student_uuid=payload['student_uuid']).first()

		if payload['tutor_uuid']:
			tutor = Tutor.query.filter_by(tutor_uuid=payload['tutor_uuid'], is_working=True, activation=True).first()

	def createSummary(self, payload, tutor_uuid):
		get_tutor = Tutor.query.filter_by(tutor_uuid=tutor_uuid, is_working=True, activation=True).first()

		if not get_tutor:
			new_summary = Student(topic = payload['topic'], email=payload['date'], \
								time_started=payload['time_started'], time_ended=payload['time_ended'], remarks=payload['remarks'], \
								sign_tutor=payload['sign_tutor'])
			new_Student.created_at = TIME
			db.session.add(new_Student)
			db.session.commit()
			return err.requestSuccess("register success")
		
		if get_student :
			return err.requestFailed("Student with that email already existed")

	def updateSummary(self, payload, student_uuid):
		get_student = Student.query.filter_by(student_uuid=student_uuid).first()

		if get_student :
			get_student.full_name    = payload['full_name']
			get_student.phone_number = payload ['phone_number']
			get_student.address		 = payload['address']
			get_student.gender		 = payload['gender']
			get_student.school	     = payload['school']
			get_student.grade		 = payload['grade']
			get_student.updated_at   = TIME
			db.session.commit()
			return err.requestSuccess("update profil success")

		if not get_student:
			return err.badRequest("not available Student")
