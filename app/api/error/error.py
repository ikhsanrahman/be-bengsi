from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

class BaseError:

  def errResponse(status_code, message=None):
      errors = {}

      if message:
        errors["error"] = message
        errors["status_code"] = status_code
      else:
        errors["error"] = HTTP_STATUS_CODES.get(status_code, 'Unknown Error'),

      return errors, status_code

class Error(BaseError):
    def requestSuccess(message=None):
        return BaseError.errResponse(200, message)

    def badRequest(message=None):
        return BaseError.errResponse(400, message)

    def requestFailed(message=None):
        return BaseError.errResponse(401, message)

