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


class Admin(db.Model):
  __tablename__ = "admin"
 
  id                        = db.Column(db.Integer, primary_key=True, autoincrement=True)
  admin_uuid                = db.Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uid())
  name                      = db.Column(db.String(255))
  password                  = db.Column(db.String(255))
  password_hash             = db.Column(db.String(255))
  time_login                = db.Column(db.DateTime)
  time_logout               = db.Column(db.DateTime)
  time_created              = db.Column(db.DateTime)


tutoring = db.Table('tutoring',
    db.Column('tutor_uuid', UUID(as_uuid=True), db.ForeignKey('tutors.tutor_uuid')),
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
  status_login            = db.Column(db.Boolean, default=True)
  activation              = db.Column(db.Boolean, default=True)
  created_at              = db.Column(db.DateTime, default=TIME)
  updated_at              = db.Column(db.DateTime) # time activated, time_reactivated,
  deleted_at              = db.Column(db.DateTime)
  time_login              = db.Column(db.DateTime, default=TIME)
  time_logout             = db.Column(db.DateTime)
  tutoring                = db.relationship('Tutor', secondary=tutoring, lazy='subquery',
                            backref=db.backref('tutoring', lazy=True))
  summary                 = db.relationship('Summary', backref='students', lazy=True)

  def generate_password_hash(self, password) :
    self.password_hash = generate_password_hash(password)

  def check_password_hash(self, password) :
    return check_password_hash(self.password_hash, password)

  def __repr__(self):
    return '<this is {}>'.format(self.full_name)

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
  created_at                  = db.Column(db.DateTime, default=TIME)
  updated_at                  = db.Column(db.DateTime)
  deleted_at                  = db.Column(db.DateTime) # time activated, time_reactivated,
  time_login                  = db.Column(db.DateTime)
  time_logout                 = db.Column(db.DateTime)
  time_tutor_on               = db.Column(db.DateTime)
  time_tutor_off              = db.Column(db.DateTime)
  time_unactivated              = db.Column(db.DateTime)
  time_reactivated            = db.Column(db.DateTime)
  subject                     = db.relationship('Subject', backref='tutors', lazy=True)
  summary                     = db.relationship('Summary', backref='tutors', lazy=True)

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
  name_subject                = db.Column(db.String(255))
  price                       = db.Column(db.Integer, default=0)
  description                 = db.Column(db.Text)
  created_at                  = db.Column(db.DateTime, default=TIME)
  updated_at                  = db.Column(db.DateTime)
  deleted_at                  = db.Column(db.DateTime)
  status                      = db.Column(db.Boolean, default=True)
  tutor                       = db.Column(UUID(as_uuid=True), db.ForeignKey('tutors.tutor_uuid'))

  def __repr__(self):
    return '< {} this subject belongs to {}>'.format(self.name_subject, self.tutor)
    

class Summary(db.Model):
  __tablename__ = "summaries"

  id                          = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
  summary_uuid                = db.Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uid())
  topic                       = db.Column(db.Text)
  date                        = db.Column(db.DateTime)
  time_started                = db.Column(db.DateTime)
  time_ended                  = db.Column(db.DateTime)
  sign_student                = db.Column(db.Boolean, default=False)
  sign_tutor                  = db.Column(db.Boolean, default=False)
  remarks                     = db.Column(db.Text)
  updated_at                  = db.Column(db.DateTime)
  deleted_at                  = db.Column(db.DateTime)
  status                      = db.Column(db.Boolean, default=False)
  student                     = db.Column(UUID(as_uuid=True), db.ForeignKey('students.student_uuid'), nullable=True)
  tutor                       = db.Column(UUID(as_uuid=True), db.ForeignKey('tutors.tutor_uuid'), nullable=True)


# class Payment(db.Model):
#   __tablename__ = "payments"

# id                          = db.Column(db.Integer, primary_key=True)
# amount_of_payment           = db.Column(db.String(255))
# time                        = db.Column(db.DateTime)
# created_at                  = db.Column(db.DateTime, default=TIME)
# updated_at                  = db.Column(db.DateTime)
# deleted_at                  = db.Column(db.DateTime)
# status                      = db.Column(db.Boolean, default=False)
# subject                     = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=True)




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