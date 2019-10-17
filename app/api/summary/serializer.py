import re

from marshmallow import Schema, fields, ValidationError, post_load, validates
from app.api.create_app import db


def cannot_be_blank(string):
  if not string:
    raise ValidationError(" Data cannot be blank")
#end def

class SummarySchema(Schema):
  id                  = fields.Int()
  topic               = fields.String(attribute="topic", required=True, validate=cannot_be_blank)
  date                = fields.DateTime(required=True, validate=cannot_be_blank)
  time_started        = fields.DateTime(required=True, validate=cannot_be_blank)
  time_ended          = fields.DateTime(required=True, validate=cannot_be_blank)
  remarks             = fields.String()
  sign_student        = fields.Boolean()
  sign_tutor          = fields.Boolean()
          
    
  @validates('topic')
  def validate_topic(self, topic):
    # allow all character
    pattern = r"^[a-z-A-Z_0-9&@#$%^*.,'?/+={}'()! ]+$"
    if len(topic) < 2:
      raise ValidationError('Invalid {}. min is 2 character'.format(topic))
    if len(topic) > 50:
      raise ValidationError('Invalid {}, max is 50 character'.format(topic))
    if re.match(pattern, topic) is None:
      raise ValidationError('Invalid {}. only alphabet is allowed'.format(topic))
  #end def

  # @validates('date')
  # def validate_date(self, date):
  #   # allow all characters except number
  #   pattern = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
  #   date = str(date)
  #   if re.match(pattern, date) is None:
  #     raise ValidationError('see the rule of options')

  # @validates('time_started')
  # def validate_time_started(self, time_started):
  #   # allow all character
  #   pattern = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
  #   time_started = str(time_started)
  #   if  re.match(pattern, time_started) is None:
  #     raise ValidationError('Invalid {}. only alphabet is allowed'.format(time_started))
  # #end def

  # @validates('time_ended')
  # def validate_time_ended(self, time_ended):
  #   # only allow alphabet character and space
  #   pattern = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
  #   time_ended=str(time_ended)
  #   if re.match(pattern, time_ended) is None:
  #     raise ValidationError('Invalid time_ended, only Human allowed to create the field, not you')
  # #end def

class UpdateTutorSchema(Schema):
  id                  = fields.Int()
  topic               = fields.String(required=True, validate=cannot_be_blank)
  date                = fields.DateTime(required=True)
  time_started        = fields.DateTime(required=True)
  time_ended          = fields.DateTime(required=True)
  remarks             = fields.String()
    
  @validates('topic')
  def validate_topic(self, topic):
    # allow all character
    pattern = r"^[a-z-A-Z_0-9,.& ]+$"

    if re.match(pattern, topic) is None:
      raise ValidationError('Invalid {}. only alphabet is allowed'.format(topic))
  #end def

  # @validates('date')
  # def validate_date(self, date):
  #   # allow all characters except number
  #   pattern = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
  #   date=str(date)
  #   if re.match(pattern, date) is None:
  #     raise ValidationError('see the rule of options')

  # @validates('time_started')
  # def validate_time_started(self, time_started):
  #   # allow all character
  #   pattern = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
  #   time_started = str(time_started)

  #   if  re.match(pattern, time_started) is None:
  #     raise ValidationError('Invalid {}}. only alphabet is allowed'.format(time_started))
  # #end def

  # @validates('time_ended')
  # def validate_time_ended(self, time_ended):
  #   # only allow alphabet character and space
  #   pattern = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
  #   time_ended = str(time_ended)
  #   if re.match(pattern, time_ended) is None:
  #     raise ValidationError('Invalid time_ended, only Human allowed to create the field, not you')
  # #end def
