from datetime import datetime, timedelta
import pytz
import secrets
import random
import uuid
import jwt

from sqlalchemy.dialects.postgresql import UUID

from werkzeug.security import generate_password_hash 
from werkzeug.security import check_password_hash

from app.api.create_app import db
from app.api.config import config

TIME = config.Config.time()

def uid():
  return uuid.uuid4()

def randomPaymentId():
  return random.randrange(1,1000)


class Admin(db.Model):
  __tablename__ = "admin"
 
  id                        = db.Column(db.Integer, primary_key=True, autoincrement=True)
  admin_uuid                = db.Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uid())
  name                      = db.Column(db.String(255))
  password                  = db.Column(db.String(255))
  password_hash             = db.Column(db.String(255))
  profit                    = db.Column(db.Integer, default=0)
  time_login                = db.Column(db.DateTime)
  time_logout               = db.Column(db.DateTime)
  time_created              = db.Column(db.DateTime)


tutoring = db.Table('tutoring',
  db.Column('subject_uuid', UUID(as_uuid=True), db.ForeignKey('subjects.subject_uuid')),
  db.Column('student_uuid', UUID(as_uuid=True), db.ForeignKey('students.student_uuid'))
)

class Student(db.Model):
  __tablename__ = "students"

  id                      = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
  student_uuid            = db.Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uid())
  full_name               = db.Column(db.String(255))
  email                   = db.Column(db.String(255))
  password                = db.Column(db.String(255))
  password_hash           = db.Column(db.String(255))
  gender                  = db.Column(db.String(255))
  grade                   = db.Column(db.String(255))
  phone_number            = db.Column(db.String(255))
  school                  = db.Column(db.String(255))
  address                 = db.Column(db.String(255))
  status_login            = db.Column(db.Boolean, default=False)
  activation              = db.Column(db.Boolean, default=True)
  created_at              = db.Column(db.DateTime, default=TIME)
  updated_at              = db.Column(db.DateTime) # time activated, time_reactivated,
  deleted_at              = db.Column(db.DateTime)
  time_login              = db.Column(db.DateTime, default=TIME)
  time_logout             = db.Column(db.DateTime)
  subscriptions           = db.relationship('Subject', secondary=tutoring, lazy='subquery',
                            backref=db.backref('subscribers', lazy="dynamic"))
  history                 = db.relationship('HistoryStudent', backref='history', lazy=True)

  def generate_password_hash(self, password) :
    self.password_hash = generate_password_hash(password)

  def check_password_hash(self, password) :
    return check_password_hash(self.password_hash, password)

  def __repr__(self):
    return '<this is {}>'.format(self.full_name)

class Subject(db.Model):
  __tablename__ = "subjects"

  id                          = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
  subject_uuid                = db.Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uid())
  subject_name                = db.Column(db.String(255))
  price                       = db.Column(db.Integer, default=0)
  description                 = db.Column(db.Text)
  created_at                  = db.Column(db.DateTime, default=TIME)
  updated_at                  = db.Column(db.DateTime)
  deleted_at                  = db.Column(db.DateTime)
  status                      = db.Column(db.Boolean, default=True)
  tutor                       = db.Column(UUID(as_uuid=True), db.ForeignKey('tutors.tutor_uuid'))
  summary                     = db.relationship('Summary', backref='owner', lazy=True)

  def __repr__(self):
    return '< {} this subject belongs to {}>'.format(self.subject_name, self.tutor)

# student and history student is one to one relationship
class HistoryStudent(db.Model):
  __tablename__ = "history_student"

  id                      = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
  history_uuid            = db.Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uid())
  subject_name            = db.Column(db.String(255))
  subject_uuid            = db.Column(UUID(as_uuid=True))
  tutor_uuid              = db.Column(UUID(as_uuid=True))
  tutor_name              = db.Column(db.String(255))
  tutor_handphone         = db.Column(db.Integer)
  date_started            = db.Column(db.DateTime)
  date_ended              = db.Column(db.DateTime)
  amount_meeting          = db.Column(db.Integer, default=0)
  amount_payment          = db.Column(db.Integer, default=randomPaymentId())
  status                  = db.Column(db.Boolean, default=True)
  created_at              = db.Column(db.DateTime, default=TIME)
  deleted_at              = db.Column(db.DateTime)
  student                 = db.Column(UUID(as_uuid=True), db.ForeignKey('students.student_uuid'), nullable=True)

  def __repr__(self):
    return '<this is {}>'.format(self.history_uuid)


class Tutor(db.Model):
  __tablename__ = "tutors"

  id                          = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
  tutor_uuid                  = db.Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uid())
  full_name                   = db.Column(db.String(255))
  email                       = db.Column(db.String(255), unique=True)
  phone_number                = db.Column(db.String(255))
  password                    = db.Column(db.String(255))
  password_hash               = db.Column(db.String(255))
  address                     = db.Column(db.String(255))
  education                   = db.Column(db.String(255))
  experience                  = db.Column(db.Text)
  gender                      = db.Column(db.String(100))
  status_login                = db.Column(db.Boolean, default=False)
  is_working                  = db.Column(db.Boolean, default=True)
  activation                  = db.Column(db.Boolean, default=False)
  number_like                 = db.Column(db.Integer, default=0)
  number_dislike              = db.Column(db.Integer, default=0)
  current_income              = db.Column(db.Integer, default=0)
  total_income                = db.Column(db.Integer, default=0)
  created_at                  = db.Column(db.DateTime, default=TIME)
  updated_at                  = db.Column(db.DateTime)
  deleted_at                  = db.Column(db.DateTime) # time activated, time_reactivated,
  time_login                  = db.Column(db.DateTime)
  time_logout                 = db.Column(db.DateTime)
  time_tutor_on               = db.Column(db.DateTime)
  time_tutor_off              = db.Column(db.DateTime)
  time_unactivated            = db.Column(db.DateTime)
  time_reactivated            = db.Column(db.DateTime)
  subject                     = db.relationship('Subject', backref='owner', lazy=True)
  history                     = db.relationship('HistoryTutor', backref='history', lazy=True)

  def generate_password_hash(self, password) :
    self.password_hash = generate_password_hash(password)

  def check_password_hash(self, password) :
    return check_password_hash(self.password_hash, password)

  def __repr__(self):
    return '<this is {}>'.format(self.full_name)
    
# Tutor and history tutor is one to one relationship    
class HistoryTutor(db.Model):
  __tablename__ = "history_tutor"

  id                      = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
  history_uuid            = db.Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uid())
  subject_name            = db.Column(db.String(255))
  subject_uuid            = db.Column(UUID(as_uuid=True))
  student_name            = db.Column(db.String(255))
  student_uuid            = db.Column(UUID(as_uuid=True))
  student_grade           = db.Column(db.String(255))
  student_school          = db.Column(db.String(255))
  student_address         = db.Column(db.Text)
  date_started            = db.Column(db.DateTime)
  date_ended              = db.Column(db.DateTime)
  amount_meeting          = db.Column(db.Integer, default=0)
  income                  = db.Column(db.Integer, default=0)
  status                  = db.Column(db.Boolean, default=True)
  created_at              = db.Column(db.DateTime, default=TIME)
  updated_at              = db.Column(db.DateTime)
  deleted_at              = db.Column(db.DateTime)
  tutor                   = db.Column(UUID(as_uuid=True), db.ForeignKey('tutors.tutor_uuid'), nullable=True)

  def __repr__(self):
    return '<this is {}>'.format(self.history_uuid)

class Summary(db.Model):
  __tablename__ = "summaries"

  id                          = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
  summary_uuid                = db.Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uid())
  subject_name                = db.Column(db.String(255))
  topic                       = db.Column(db.Text)
  date                        = db.Column(db.DateTime)
  time_started                = db.Column(db.DateTime)
  time_ended                  = db.Column(db.DateTime)
  sign_student                = db.Column(db.Boolean, default=False)
  sign_tutor                  = db.Column(db.Boolean, default=False)
  remarks                     = db.Column(db.Text)
  created_at                  = db.Column(db.DateTime, default=TIME)
  updated_at                  = db.Column(db.DateTime)
  deleted_at                  = db.Column(db.DateTime)
  status                      = db.Column(db.Boolean, default=True)
  subject                     = db.Column(UUID(as_uuid=True), db.ForeignKey('subjects.subject_uuid'), nullable=True)
  
  def __repr__(self):
    return '<this is {}>'.format(self.topic, self.subject)



# class BlacklistToken(db.Model):
#     """
#     Token Model for storing JWT tokens
#     """
#     __tablename__ = 'blacklist_tokens'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     token = db.Column(db.String(500), unique=True, nullable=False)
#     blacklisted_on = db.Column(db.DateTime, nullable=False)

#     def __init__(self, token):
#         self.token = token
#         self.blacklisted_on = TIME

#     def __repr__(self):
#         return '<id: token: {}'.format(self.token)

#     @staticmethod
#     def check_blacklist(auth_token):
#         # print(type(auth_token))
#         # check whether auth token has been blacklisted
#         # print(auth_token)
#         res = BlacklistToken.query.filter_by(token=auth_token).first()
#         print(res)
#         print('wew')
#         if res:
#             return True
#         else:
#             return False