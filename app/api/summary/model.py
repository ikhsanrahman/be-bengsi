from app.api.create_app import db 
from app.api.db_model import *
from app.api.student.serializer import StudentSchema
from app.api.error import error
from flask import jsonify

from app.api.config.config import Config

TIME = Config.time()
err = error.Error

class SummaryProcess:

	def getSummaries(self):
		students = Student.query.filter_by(status=True).all()
		result = StudentSchema(many=True).dump(students).data
		if students :
			return jsonify(result)

		if not students:
			return err.requestFailed("no student available")
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

	def removeStudent(self, student_uuid):
		get_student = Student.query.filter_by(student_uuid=student_uuid).first()

		if get_student :
			db.session.delete(get_student)
			db.session.commit()
			return err.requestSuccess("remove Student has succeed")
		if not get_student:
			return err.requestFailed("no Student available")

	def updatePassword(self, payload, student_uuid):
		get_student = Student.query.filter_by(student_uuid=student_uuid, email=payload['email']).first()

		if student:
			student.password = payload['new_password']
			student.generate_password_hash(payload['new_password'])
			student.updated_at = TIME
			db.session.commit()
			return err.requestSuccess("edit password success")

		if not Student:
			return err.requestFailed("Student is not available")


	def forgetPassword(self, payload):
		student = Student.query.filter_by(email=payload['email']).first()

		if student:
			student.password = payload['new_password']
			student.generate_password_hash(payload['new_password'])
			student.updated_at = TIME
			db.session.commit()
			return err.requestSuccess("edit forget password success")

		if not Student:
			return err.requestFailed("Student is not available")

	def loginStudent(self, payload):
		student = Student.query.filter_by(email=payload['email'], status=False).first()
		if student and student.check_password_hash(payload['password']):
			student.status = True
			student.time_login = TIME
			db.session.commit()
			result = StudentSchema().dump(student).data
			return jsonify(result)
		return err.requestFailed("login failed")

	def logoutStudent(self, student_uuid):
		student = Student.query.filter_by(student_uuid=student_uuid, status=True).first()
		print	(student, student_uuid)
		if student:
			student.status = False
			Student.time_logout = TIME
			db.session.commit()
			return err.requestSuccess('logout success')

		return err.requestFailed("logout failed")

	def unactivateStudent(self, student_uuid):
		student = Student.query.filter_by(student_uuid=student_uuid).first()
		if student :
			student.status = False
			db.session.commit()
			return err.requestSuccess("unactivate Student success")
		if not student :
			return err.requestFailed("no Student can be unactivated")

	def reactivateStudent(self, student_uuid):
		student = Student.query.filter_by(student_uuid=student_uuid).first()
		if student :
			if student.status == True:
				return err.requestFailed("Student already active")
			if student.status == False:
				student.status = True
				db.session.commit()
				return err.requestSuccess("reactivate Student has succeed")
		
		if not Student:
			return err.badRequest("seller is not available")

	def searchStudentByName(self, payload):
		fetchStudents = Student.query.all()
		result = []
		for student in fetchStudents :
			if payload['name'] in student.full_name :
				Student_ = StudentSchema().dump(student).data
				result.append(Student_)
		if result:
			return result

		return err.badRequest("No Student detected")
