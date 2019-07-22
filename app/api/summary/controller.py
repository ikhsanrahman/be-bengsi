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


@api.route('')
class Summary(Resource):
  @api.doc('get all Summary')
  def get(self):

    result = summaryProcess().getSummaries() 
    return result

  @api.doc('Create new summary')
  def post(self):
      payload = RegisterSummaryRequestSchema().parser.parse_args(strict=True)

      errors = SummarySchema().load(payload).errors
      if errors :
          return errors

      result = SummaryProcess().createSummary(payload)
      return result


@api.route('/<string:summary_uuid>/updatesummary')
class UpdateSummary(Resource):
    
    @api.doc('update a summary')
    def put(self, summary_uuid):
       
        payload = UpdateSummaryRequestSchema().parser.parse_args(strict=True)

        errors = UpdateSummarySchema().load(payload).errors
        if errors :
            return errors

        updateSummary = SummaryProcess().updateSummary(payload, summary_uuid)
        return updateSummary
