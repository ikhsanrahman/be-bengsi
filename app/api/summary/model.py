from app.api.create_app import db 
from app.api.db_model import *
from app.api.student.serializer import StudentSchema
from app.api.tutor.subject.serializer import SubjectSchema
from app.api.student.serializer import StudentSchema
from app.api.summary.serializer import SummarySchema
from app.api.error import error
from flask import jsonify

from app.api.config.config import Config

TIME = Config.time()
err = error.Error

class SummaryProcess:

	def getSummaries(self, payload):
		get_tutor = Tutor.query.filter_by(tutor_uuid=payload['tutor_uuid'], activation=True, is_working=True,\
			status_login=True).first()

		get_student = Student.query.filter_by(student_uuid=payload['student_uuid'], status_login=True, \
			activation=True).first()

		if get_tutor:
			responses = {}
			responses['records'] = []
			contain = {}
			get_subject = Subject.query.filter_by(subject_uuid=payload['subject_uuid'], \
				subject_name=payload['subject_name'], tutor=get_tutor.tutor_uuid).first()
			if get_subject:
				if get_subject in get_tutor.subject:
					contain['subject_name'] = get_subject.subject_name
					get_summary = SummarySchema(many=True).dump(get_subject.summary).data
					contain['summary'] = get_summary
					responses['records'].append(contain)
					return responses
				if not get_subject in get_tutor.subject:
					return err.requestFailed("the tutor has no such subject")
			if not get_subject:
				return err.requestFailed("there is no such subject")
		if not get_tutor:
			return err.badRequest("this account has no access in this page")	

		if get_student in get_subject.subscribers:
			responses = {}
			responses['records'] = []
			contain = {}
			contain['subject_name'] = get_subject.subject_name
			get_summary = SummarySchema(many=True).dump(get_subject.summary).data
			contain['summary'] = get_summary
			responses['records'].append(contain)
			return responses
		if not get_student in get_subject.subscribers:
			return err.badRequest('that student has not such subject')

	# tutor can know their student and subject and vice versa
	def getTutorStudentSubject(self, payload):
		if payload['student_uuid']:
			result = []
			data = {}
			student = Student.query.filter_by(student_uuid=payload['student_uuid']).first()
			if student:
				for subject in student.subscriptions:
					data['subject'] = subject.subject_name
					data['subject_uuid'] = str(subject.subject_uuid)
					data['name_tutor'] = subject.owner.full_name
					data['tutor_handphone'] = subject.owner.phone_number
					data['tutor_uuid'] = str(subject.owner.tutor_uuid)
					data['tutor_activation'] =  subject.owner.activation
					data['tutor_is_working'] = subject.owner.is_working
					result.append(dict(data))
			if result:
				return result
			if not result:
				return err.requestFailed("you dont have any subject and tutor")

		if payload['tutor_uuid']:
			responses = {}
			responses['records'] = []
			contain = {}
			contain['student'] = []
			get_tutor = Tutor.query.filter_by(tutor_uuid=payload['tutor_uuid'], is_working=True, activation=True).first()
			for subject in get_tutor.subject:
				contain['subject_name'] = subject.subject_name
				contain['subject_uuid'] = str(subject.subject_uuid)
				result = StudentSchema(many=True).dump(subject.subscribers).data
				if len(result) > 0:
					contain['student'] = result

				if len(result) == 0:
					contain['student'] = []

				responses['records'].append(dict(contain))
			return responses

	# student tanda tangan
	def signStudent(self, payload):

		if payload['student_uuid'] and payload['subject_uuid'] and payload['summary_uuid'] and payload['tutor_uuid']:
			get_student = Student.query.filter_by(student_uuid=payload['student_uuid'], status_login=True,\
			 activation=True).first()
			get_tutor = Tutor.query.filter_by(tutor_uuid=payload['tutor_uuid'], is_working=True, activation=True\
				).first()
			get_subject = Subject.query.filter_by(subject_uuid=payload['subject_uuid'], tutor=get_tutor.tutor_uuid,\
				status=True).first()
			get_summary = Summary.query.filter_by(summary_uuid=payload['summary_uuid'], status=True,\
				subject=get_subject.subject_uuid).first()
			history_student = HistoryStudent.query.filter_by(subject_uuid=str(get_subject.subject_uuid), \
				subject_name=get_subject.subject_name, student=get_student.student_uuid, status=True, \
				tutor_uuid=str(get_tutor.tutor_uuid)).first()
			history_tutor = HistoryTutor.query.filter_by(subject_uuid=get_subject.subject_uuid, \
				subject_name=get_subject.subject_name, tutor=get_tutor.tutor_uuid, status=True).first()

			if get_student:
				if get_subject in get_student.subscriptions:
					if get_summary:

						get_summary.sign_student = True
						db.session.commit()

						if not history_student and history_tutor:
							new_history = HistoryStudent(subject_name=get_subject.subject_name, subject_uuid=get_subject.subject_uuid, \
								tutor_name=get_tutor.full_name, tutor_uuid=get_tutor.tutor_uuid, \
								tutor_handphone=get_tutor.phone_number, amount_payment=get_subject.price, \
								student=get_student.student_uuid)
							new_history.created_at = TIME
							new_history.date_started = TIME
							new_history.amount_meeting = 1
							new_history.amount_payment = get_subject.price
							db.session.add(new_history)

							history_tutor.income = (get_subject.price - 15000)

							get_tutor.current_income = (get_subject.price - 15000)
							get_tutor.total_income = get_tutor.current_income

						if history_student and history_tutor:
							history_student.amount_meeting += 1

							history_tutor.income += (get_subject.price - 15000)

							get_tutor.current_income += (get_subject.price - 15000)
							get_tutor.total_income += get_tutor.current_income
							
						db.session.commit()
						return err.requestSuccess("the meeting has signed successfully")

					if not get_summary:
						return err.requestFailed("can not sign the summary")

				if not get_subject in get_student.subscriptions:
					return err.requestFailed(get_student + ' ' + "has no that subject," + get_subject.name_subject)

			if get_summary and get_subject and get_student:
				return err.requestFailed("can not has access to sign")

		if not payload['student_uuid'] and payload['subject_uuid'] and payload['summary_uuid']:
			return err.badRequest("no having access to do action")

	# tutor only can create new summary
	def createSummary(self, payload, tutor_uuid):
		
		get_tutor = Tutor.query.filter_by(tutor_uuid=tutor_uuid, status_login=True, is_working=True, \
			activation=True).first()
		
		if get_tutor:
			get_subject = Subject.query.filter_by(subject_uuid=payload['subject_uuid'], \
				tutor=get_tutor.tutor_uuid).first()
			get_summary = Summary.query.filter_by(date=payload['date'], subject=get_subject.subject_uuid).first()
			get_student = Student.query.filter_by(student_uuid=payload['student_uuid'], activation=True).first()
			history_tutor = HistoryTutor.query.filter_by(subject_uuid=get_subject.subject_uuid, \
				subject_name=get_subject.subject_name, tutor=get_tutor.tutor_uuid, status=True).first()

			if get_subject in get_tutor.subject and get_subject in get_student.subscriptions:
				if not get_summary in get_subject.summary or get_summary in get_subject.summary:
					if not get_summary:
						new_summary = Summary(subject_name=get_subject.subject_name, topic = payload['topic'], \
							date=payload['date'], time_started=payload['time_started'], \
							time_ended=payload['time_ended'], remarks=payload['remarks'], \
							subject=get_subject.subject_uuid)
						new_summary.created_at = TIME
						new_summary.sign_tutor = True
						db.session.add(new_summary)
						db.session.commit()
						
						if not history_tutor:
							new_history = HistoryTutor(subject_name=get_subject.subject_name, subject_uuid=str(get_subject.subject_uuid), \
								student_name=get_student.full_name, student_uuid=str(get_student.student_uuid), \
								student_grade=get_student.grade, student_school=get_student.school, \
								student_address=get_student.address, tutor=get_tutor.tutor_uuid)
							new_history.created_at = TIME
							new_history.date_started = TIME
							new_history.amount_meeting = 1
							db.session.add(new_history)
							db.session.commit()

						if history_tutor:
							history_tutor.amount_meeting += 1
							db.session.commit()

						return err.requestSuccess("Create summary success")

					if get_summary :
						return err.badRequest("can not create summary on same date")

			if not get_subject in get_tutor.subject:
				return err.requestFailed("tutor has not that subject, "+ get_subject.name_subject)
				
		if not get_tutor or not get_student :
			return err.requestFailed("tutor has no access to create a new summary")

	#tutor only can update the summary
	def updateSummary(self, payload, tutor_uuid):
		if payload['summary_uuid']:
			get_tutor = Student.query.filter_by(tutor_uuid=tutor_uuid, status_login=True, activation=True, \
				is_working=True).first()

			get_subject = Subject.query.filter_by(subject_uuid=payload['subject_uuid'], tutor=get_tutor.tutor_uuid \
				).first()

			get_summary = Summary.query.filter_by(summary_uuid=payload['summary_uuid'], sign_student=True,\
				status=True).first()

			get_student = Student.query.filter_by(student_uuid=payload['student_uuid'], activation=True).first()
			
			history_tutor = HistoryTutor.query.filter_by(subject_uuid=get_subject.subject_uuid, \
				subject_name=get_subject.subject_name, tutor=get_tutor.tutor_uuid, status=True).first()

			history_student = HistoryStudent.query.filter_by(subject_name=get_subject.subject_name, \
				subject_uuid=get_subject.subject_uuid, tutor_uuid=get_tutor.tutor_uuid, \
				student = get_student.student_uuid).first()

			if get_tutor:
				if get_subject in get_tutor.subject and get_subject in get_student.subscriptions:
					if get_summary in get_subject.summary:
						get_summary.topic = payload['topic']
						get_summary.date = payload['date']
						get_summary.time_started = payload['time_started']
						get_summary.time_ended = payload['time_ended']
						get_summary.remarks = payload['remarks']
						get_summary.update_at = TIME
						db.session.commit()

						sumarries = Summary.query.order_by(Summary.date).first()
						if get_summary == summaries[0]:
							history_tutor.date_started = payload['date']
							db.session.commit()
							history_student.date_started = payload['date']

						return err.requestSuccess("update summary success")
			
					if not get_summary in get_subject.summary:
						return err.requestFailed('the subject has no summary')
				else:
					return err.badRequest("tutor have no that subject")		
			if not get_tutor:
				return err.requestFailed("can not have access to update summary")
		
		if not payload['tutor_uuid'] and payload['summary_uuid']:
			return err.badRequest("not available tutor and summary to do action")
