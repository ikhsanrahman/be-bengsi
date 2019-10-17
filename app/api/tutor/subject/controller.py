import datetime
import jwt

from flask import request, make_response, jsonify
from flask_restplus import Resource

from app.api.tutor.subject.serializer import *
from app.api.tutor.subject.model import SubjectProcess
from app.api.tutor.subject.request_schema import *
from app.api.config import config
from app.api.error import error
from app.api.namespace import Subject

api = Subject.api
err = error.Error

@api.route('/search')
class SearchSubject(Resource) :

  @api.doc('search subject by name')
  def get(self) :
    payload = SearchSubjectNameRequestSchema().parser.parse_args(strict=True)

    search = SubjectProcess().searchSubjectByName(payload)
    return search

@api.route('')
class Subject(Resource):
  @api.doc('get all subjects')
  def get(self):

    result = SubjectProcess().getSubjects()
    return result

@api.route('/<string:tutor_uuid>/createsubject')
class Subject(Resource):
  @api.doc('registering new subject')
  def post(self, tutor_uuid):
      
    payload = RegisterSubjectRequestSchema().parser.parse_args(strict=True)

    errors = SubjectSchema().load(payload).errors
    if errors :
      return errors

    result = SubjectProcess().createSubject(payload, tutor_uuid)
    return result

@api.route('/<string:tutor_uuid>/tutor/<string:subject_uuid>/subject')
class Subject(Resource):
  @api.doc('update a subject')
  def put(self, tutor_uuid, subject_uuid):
    payload = UpdateSubjectRequestSchema().parser.parse_args(strict=True)

    errors = UpdateSubjectSchema().load(payload).errors
    if errors :
      return errors

    updateSubject = SubjectProcess().updateSubject(payload, tutor_uuid, subject_uuid)
    return updateSubject

@api.route('/<string:subject_uuid>/unactivate')
class UnactivateSubject(Resource):

  @api.doc('unactivate a subject')
  def get(self, subject_uuid):
    result = SubjectProcess().unactivateSubject(subject_uuid)
    return result

@api.route('/<string:subject_uuid>/reactivate')
class ReactivateSubject(Resource) :
      
  def get(self, subject_uuid) :
    result = SubjectProcess().reactivateSubject(subject_uuid)
    return result
