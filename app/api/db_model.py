


class Admin(db.Model):
	__tablename__ = "admin"

	id                        = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name                      = db.Column(db.String(255))
	password                  = db.Column(db.String(255))
	password_hash             = db.Column(db.String(255))
	time_login                = db.Column(db.DateTime)
	time_logout               = db.Column(db.DateTime)
	time_created              = db.Column(db.DateTime)



class Student(db.Model):
	__tablename__ = "students"

	id						              = db.Column(db.Integer, primary_key=True, autoincrement=True) 
	name					              = db.Column(db.String(255))
	email					              = db.Column(db.String(255))
	password				            = db.Column(db.String(255))
	password_hash			          = db.Column(db.String(255))
	grade 					            = db.Column(db.String(255))
	school					            = db.Column(db.String(255))
	address					            = db.Column(db.String(255))
	status					            = db.Column(db.Boolean, default=True)
	create_at                   = db.Column(db.DateTime, default=TIME)
  updated_at                  = db.Column(db.DateTime)
  deleted_at                  = db.Column(db.DateTime)
  time_login                  = db.Column(db.DateTime)
  time_logout                 = db.Column(db.DateTime)


class Tutor(db.Model):
	__tablename__ = "tutors"

	id                          = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name                        = db.Column(db.String(255))
	email                       = db.Column(db.String(255), unique=True)
	password                    = db.Column(db.String(255))
	password_hash               = db.Column(db.String(255))
	address                     = db.Column(db.String(255))
	education                   = db.Column(db.String(255))
	status                      = db.Column(db.Boolean, default=False)
  amount_like                 = db.Column(db.Integer, default=0)
  amount_dislike              = db.Column(db.Integer, default=0)
	created_at                  = db.Column(db.DateTime, default=TIME)
  updated_at                  = db.Column(db.DateTime)
  deleted_at                  = db.Column(db.DateTime)
  time_login                  = db.Column(db.DateTime)
  time_logout                 = db.Column(db.DateTime)
  subject                     = db.relationship('Subject', backref='tutors', lazy=True)


class Subject(db.Model):
  __tablename__ = "subjects"

	id                          = db.Column(db.Integer, primary_key=True)
  name_subject                = db.Column(db.String(255))
  amount_like                 = db.Column(db.Integer, default=0)
  amount_dislike              = db.Column(db.Integer, default=0)
	created_at                  = db.Column(db.DateTime, default=TIME)
  updated_at                  = db.Column(db.DateTime)
  deleted_at                  = db.Column(db.DateTime)
	status                      = db.Column(db.Boolean, default=False)
  tutor                       = db.Column(db.Integer, db.ForeignKey('tutors.id'), nullable=True)
  schedule                    = db.relationship('Schedule', backref='subjects', lazy=True)
    

class Schedule(db.Model):
  __tablename__ = "schedules"

id                          = db.Column(db.Integer, primary_key=True)
day                         = db.Column(db.String(255))
time                        = db.Column(db.DateTime)
created_at                  = db.Column(db.DateTime, default=TIME)
updated_at                  = db.Column(db.DateTime)
deleted_at                  = db.Column(db.DateTime)
status                      = db.Column(db.Boolean, default=False)
subject                     = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=True)


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




class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = TIME

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # print(type(auth_token))
        # check whether auth token has been blacklisted
        # print(auth_token)
        res = BlacklistToken.query.filter_by(token=auth_token).first()
        print(res)
        print('wew')
        if res:
            return True
        else:
            return False