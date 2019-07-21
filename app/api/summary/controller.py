import datetime
import jwt

from flask import request, make_response, jsonify
from flask_restplus import Resource

from app.api.student.serializer import *
from app.api.student.model import StudentProcess
from app.api.student.request_schema import *
from app.api.config import config
from app.api.error import error
from app.api.namespace import Student, Home

api = Student.api
home = Home.api
err = error.Error

@home.route('')
class Home(Resource):
  def get(self) :
    responses = {}
    responses['Entry Gate'] = "Welcome to Tutor Private Platform " 
    return jsonify(Opening=responses)
     
@api.route('/login')
class StudentLogin(Resource) :
  def get(self):
    payload = LoginStudentRequestSchema().parser.parse_args(strict=True)
    if payload['password'] != payload['confirm_password']:
        return err.badRequest("password doesnt not match")
        
    errors = LoginStudentSchema().load(payload).errors
    if errors:
        return errors

    result = StudentProcess().loginStudent(payload)
    return result

@api.route('/<string:student_uuid>/logout')
class StudentLogout(Resource) :
  def get(self, student_uuid):

    logout = StudentProcess().logoutStudent(student_uuid)
    return logout

@api.route('/search')
class SearchNameStudent(Resource) :

  @api.doc('search student by name')
  def get(self) :
    payload = SearchStudentNameRequestSchema().parser.parse_args(strict=True)

    searchStudent = StudentProcess().searchStudentByName(payload)
    return searchStudent


@api.route('')
class Student(Resource):
  @api.doc('get all Student')
  def get(self):

    result = StudentProcess().getStudents() 
    return result

  @api.doc('registering new Student')
  def post(self):
      
      payload = RegisterStudentRequestSchema().parser.parse_args(strict=True)

      errors = StudentSchema().load(payload).errors
      if errors :
          return errors

      result = StudentProcess().createStudent(payload)
      return result

  def patch(self):
      payload = ForgetPasswordRequestSchema().parser.parse_args(strict=True)
      errors = ForgetPasswordSchema().load(payload).errors
      if errors:
          return errors

      result = StudentProcess().forgetPassword(payload)
      return result

@api.route('/<string:student_uuid>')
class UpdateDeleteStudent(Resource):
    
    @api.doc('update a Student')
    def put(self, student_uuid):
       
        payload = UpdateStudentRequestSchema().parser.parse_args(strict=True)

        errors = UpdateStudentSchema().load(payload).errors
        if errors :
            return errors

        updateStudent = StudentProcess().updateStudent(payload, student_uuid)
        return updateStudent

    @api.doc('remove a Student')
    def delete(self, student_uuid):
        result = StudentProcess().unactivateStudent(student_uuid)
        return result


@api.route('/<string:student_uuid>/updatepassword')
class UpdatePasswordStudent(Resource):
    
    @api.doc('update password Student')
    def patch(self, student_uuid):
       
        payload = UpdatePasswordRequestSchema().parser.parse_args(strict=True)

        if payload['new_password'] != payload['confirm_new_password'] :
            return err.requestFailed("password doesnt match")

        errors = UpdatePasswordSchema().load(payload).errors
    
        if errors :
            return errors

        updatePassword = StudentProcess().updatePassword(payload, student_uuid)
        return updatePassword
    #end def

@api.route('/<string:student_uuid>/reactivate')
class ReactivateStudent(Resource) :
      
    def get(self, student_uuid) :
        result = StudentProcess().reactivateStudent(student_uuid)
        return result
