from flask_restplus import Api
from flask import Blueprint

from app.api.student.controller import api as student
from app.api.student.controller import home as home
from app.api.tutor.controller import api as tutor
from app.api.summary.controller import api as summary
# from app.api.admin.controller import api as admin
from app.api.tutor.subject.controller import api as subject
# from app.api.buyer.controller import api as buyer

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Tutor Backend ',
          version='1.0',
          description='API for tutor hub'
          )

 
api.add_namespace(home, path='/')
api.add_namespace(student, path='/student')
api.add_namespace(tutor, path='/tutor')
api.add_namespace(subject, path='/subject')
api.add_namespace(summary, path='/summary')
# api.add_namespace(admin, path='/admin')