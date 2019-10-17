import re

from marshmallow import Schema, fields, ValidationError, post_load, validates
from app.api.create_app import db


def cannot_be_blank(string):
  if not string:
    raise ValidationError(" Data cannot be blank")
#end def

class SubjectSchema(Schema):
  id                  = fields.Int()
  subject_uuid        = fields.UUID(attribute="subject_uuid")
  subject_name        = fields.String(required=True, validate=cannot_be_blank)
  price               = fields.String(required=True, validate=cannot_be_blank)
  description         = fields.String(required=True, validate=cannot_be_blank)
  status              = fields.Method("bool_to_status")
  created_at          = fields.DateTime()
  updated_at          = fields.DateTime()
  deleted_at          = fields.DateTime()
  tutor               = fields.UUID(attribute="tutor")
        
    
  def bool_to_status(self, obj):
    status = "ACTIVE"
    if obj.status == False:
      status = "INACTIVE"
    return status

  @validates('subject_name')
  def validate_subject_name(self, subject_name):
    # allow all character
    pattern = r"^[a-z-A-Z_0-9 ]+$"
    if len(subject_name) < 2:
      raise ValidationError('Invalid {}. min is 2 character'.format(subject_name))
    if len(subject_name) > 40:
      raise ValidationError('Invalid {}, max is 40 character'.format(subject_name))
    if re.match(pattern, subject_name) is None:
      raise ValidationError('Invalid {}.'.format(subject_name))
  #end def

  @validates('price')
  def validate_price(self, price):
    # allow all characters except number
    pattern = r"^[0-9]+$"
    if len(price) < 2:
      raise ValidationError('Invalid price, min is 2 characters')
    if len(price) > 40:
      raise ValidationError('Invalid price, min is 40 character')
    if re.match(pattern, price) is None:
      raise ValidationError('see the rule of price')

  @validates('description')
  def validate_description(self, description):
    # only allow alphabet character and space
    pattern = r"^[a-z-A-Z_0-9. ]+$"
    if len(description) < 2:
      raise ValidationError('Invalid description')
    if len(description) > 20:
      raise ValidationError('Invalid description, max is 20 character')
    if re.match(pattern, description) is None:
      raise ValidationError('Invalid description')


class UpdateSubjectSchema(Schema):
  id                  = fields.Int()
  subject_uuid        = fields.String(attribute="subject_uuid")
  subject_name        = fields.String(required=True, validate=cannot_be_blank)
  price               = fields.String(required=True, validate=cannot_be_blank)
  description         = fields.String(required=True, validate=cannot_be_blank)
  status              = fields.Method("bool_to_status")
  created_at          = fields.DateTime()
  updated_at          = fields.DateTime()
  deleted_at          = fields.DateTime()
        
    
  def bool_to_status(self, obj):
    status = "ACTIVE"
    if obj.status == False:
      status = "INACTIVE"
    return status

  @validates('subject_name')
  def validate_subject_name(self, subject_name):
    # allow all character
    pattern = r"^[a-z-A-Z_0-9 ]+$"
    if len(subject_name) < 2:
      raise ValidationError('Invalid {}. min is 2 character'.format(subject_name))
    if len(subject_name) > 40:
      raise ValidationError('Invalid {}, max is 40 character'.format(subject_name))
    if re.match(pattern, subject_name) is None:
      raise ValidationError('Invalid {}.'.format(subject_name))
  #end def

  @validates('price')
  def validate_price(self, price):
    # allow all characters except number
    pattern = r"^[0-9]+$"
    if len(price) < 2:
      raise ValidationError('Invalid price, min is 2 characters')
    if len(price) > 40:
      raise ValidationError('Invalid price, min is 40 character')
    if re.match(pattern, price) is None:
      raise ValidationError('see the rule of price')

  @validates('description')
  def validate_gender(self, description):
    # only allow alphabet character and space
    pattern = r"^[a-z-A-Z_0-9. ]+$"
    if len(description) < 2:
      raise ValidationError('Invalid description')
    if len(description) > 20:
      raise ValidationError('Invalid description, max is 20 character')
    if re.match(pattern, description) is None:
      raise ValidationError('Invalid description')
  #end def
