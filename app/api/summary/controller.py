import datetime
import jwt

from flask import request, make_response, jsonify
from flask_restplus import Resource

from app.api.summary.serializer import *
from app.api.summary.model import SummaryProcess
from app.api.summary.request_schema import *
from app.api.config import config
from app.api.error import error
from app.api.namespace import Summary

api = Summary.api
err = error.Error


@api.route('/info')
class GetInfoTutorOrStudent(Resource):
  # student can switch and see subject, tutor and vice versa
  @api.doc('get info')
  def get(self):
    payload = GetSummariesRequestSchema().parser.parse_args(strict=True)

    result = SummaryProcess().getTutorStudentSubject(payload) 
    return result

@api.route('/getsummaries')
class GetInfoTutorOrStudent(Resource):
  # student can see their summary based on subject which has been switched
  @api.doc('get all summaries')
  def get(self):
    payload = GetSummariesRequestSchema().parser.parse_args(strict=True)

    result = SummaryProcess().getSummaries(payload) 
    return result

@api.route('/signstudent')
class SignStudent(Resource):
  @api.doc('sign by student')
  def get(self):
    payload = GetSummariesRequestSchema().parser.parse_args(strict=True)

    result = SummaryProcess().signStudent(payload) 
    return result

@api.route('/<string:tutor_uuid>/tutor/createsummary')
class CreatingSummary(Resource):
  @api.doc('Create new summary')
  def post(self, tutor_uuid):

    payload = RegisterSummaryRequestSchema().parser.parse_args(strict=True)
    errors = SummarySchema().load(payload).errors
    if errors :
        return errors

    result = SummaryProcess().createSummary(payload, tutor_uuid)
    return result

@api.route('/<string:tutor_uuid>/updatesummary')
class UpdateSummary(Resource):
    
    @api.doc('update a summary')
    def put(self, tutor_uuid):
       
        payload = UpdateSummaryRequestSchema().parser.parse_args(strict=True)

        errors = UpdateSummarySchema().load(payload).errors
        if errors :
            return errors

        updateSummary = SummaryProcess().updateSummary(payload, tutor_uuid)
        return updateSummary
