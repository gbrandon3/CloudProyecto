
from datetime import datetime
from sqlite3 import IntegrityError

from flask import request
from model import db
from flask import request
from flask_restful import Resource
class TaskView(Resource):
    def post(self):
        
        print(type (request.files['file']))