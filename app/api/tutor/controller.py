import datetime
import jwt

from flask import request, make_response, jsonify
from flask_restplus import Resource

from app.api.tutor.serializer import *
from app.api.tutor.model import TutorProcess
from app.api.tutor.request_schema import *
from app.api.config import config
from app.api.error import error
from app.api.namespace import Tutor

api = Tutor.api
err = error.Error

     
@api.route('/login')
class TutorLogin(Resource) :
  def get(self):
    payload = LoginTutorRequestSchema().parser.parse_args(strict=True)
    if payload['password'] != payload['confirm_password']:
        return err.badRequest("password doesnt not match")
        
    errors = LoginTutorSchema().validate(payload)

    if errors:
        return errors

    result = TutorProcess().loginTutor(payload)
    return result

@api.route('/<string:tutor_uuid>/logout')
class TutorLogout(Resource) :
  def get(self, tutor_uuid):

    logout = TutorProcess().logoutTutor(tutor_uuid)
    return logout

@api.route('/<string:tutor_uuid>/isworking')
class StatusWorking(Resource) :
  def get(self, tutor_uuid):
    payload = TutorIsWorkingRequestSchema().parser.parse_args(strict=True)

    tutorOn = TutorProcess().statusWorking(payload, tutor_uuid)
    return tutorOn

@api.route('/search')
class SearchNameTutor(Resource) :

  @api.doc('search tutor by name')
  def get(self) :
    payload = SearchTutorNameRequestSchema().parser.parse_args(strict=True)

    searchTutor = TutorProcess().searchTutorByName(payload)
    return searchTutor

@api.route('/showtutor')
class ShowTutorSubject(Resource):
  def get(self):
    result = TutorProcess().showTutor()
    return result

@api.route('')
class Tutor(Resource):
  @api.doc('get all tutor')
  def get(self):
    payload = GetTutorRequestSchema().parser.parse_args(strict=True)

    result = TutorProcess().getTutors(payload) 
    return result

  @api.doc('registering new tutor')
  def post(self):
      
    payload = RegisterTutorRequestSchema().parser.parse_args(strict=True)

    errors = TutorSchema().validate(payload)
    
    if errors :
        return errors

    result = TutorProcess().createTutor(payload)
    return result

  @api.doc('tutor forget password')
  def patch(self):
      payload = ForgetPasswordRequestSchema().parser.parse_args(strict=True)
      errors = ForgetPasswordSchema().validate(payload)
      if errors:
          return errors

      result = TutorProcess().forgetPassword(payload)
      return result

# UPDATE and UNACTIVATE TUTOR
@api.route('/<string:tutor_uuid>/updateprofile')
class UpdateProfileTutor(Resource):
    
  @api.doc('update a profile tutor')
  def put(self, tutor_uuid):
     
    payload = UpdateTutorRequestSchema().parser.parse_args(strict=True)

    errors = UpdateTutorSchema().validate(payload)
    if errors :
      return errors

    updateTutor = TutorProcess().updateTutor(payload, tutor_uuid)
    return updateTutor

@api.route('/<string:tutor_uuid>/reactivate')
class UnactivateTutor(Resource):
  @api.doc('unactivateTutor a tutor')
  def get(self, tutor_uuid):
    result = TutorProcess().unactivateTutor(tutor_uuid)
    return result


@api.route('/<string:tutor_uuid>/updatepassword')
class UpdatePasswordTutor(Resource):
    
    @api.doc('update password tutor')
    def patch(self, tutor_uuid):
       
        payload = UpdatePasswordRequestSchema().parser.parse_args(strict=True)

        if payload['new_password'] != payload['confirm_new_password'] :
            return err.requestFailed("password doesnt match")

        errors = UpdatePasswordSchema().validate(payload)
    
        if errors :
            return errors

        updatePassword = TutorProcess().updatePassword(payload, tutor_uuid)
        return updatePassword
    #end def

@api.route('/<string:tutor_uuid>/reactivate')
class ReactivateTutor(Resource) :
      
  @api.doc('reactivate tutor')
  def get(self, tutor_uuid) :
    result = TutorProcess().reactivateTutor(tutor_uuid)
    return result
