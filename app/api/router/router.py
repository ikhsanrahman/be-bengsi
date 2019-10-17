from flask_restplus import Api
from flask import Blueprint

from app.api.student.controller import api as student
from app.api.tutor.controller import home as home
# from app.api.item.controller import api as item
# from app.api.admin.controller import api as admin
from app.api.product.controller import api as product
from app.api.buyer.controller import api as buyer

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='KRISFI API ',
          version='1.0',
          # description='a engine to score object'
          )

 
api.add_namespace(home, path='/')
api.add_namespace(seller, path='/seller')
api.add_namespace(item, path='/item')
api.add_namespace(product, path='/product')
api.add_namespace(buyer, path='/buyer')
# api.add_namespace(admin, path='/admin')