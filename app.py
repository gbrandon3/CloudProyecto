from datetime import timedelta
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS
from model import db
from view import SignUpView, SignInView, TaskView, TasksView, TaskViewFile
import app_settings
from view.convertView import ConvertView

app = Flask(__name__)
                                                
app.config['SQLALCHEMY_DATABASE_URI'] = app_settings.SQLALCHEMY_DATABASE_URI

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['UPLOADED_FILES_DEST'] = 'uploads'
app_context = app.app_context()

app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)

api.add_resource(SignUpView, "/api/auth/signup")
api.add_resource(SignInView, "/api/auth/signin")
api.add_resource(TasksView, "/api/tasks")
api.add_resource(TaskView, "/api/task/<int:id_task>")
api.add_resource(TaskViewFile, "/api/file/<string:file_name>")
api.add_resource(ConvertView, "/api/convert")
jwt = JWTManager(app)
