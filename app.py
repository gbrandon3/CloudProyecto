from datetime import timedelta
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS
from model import db
from view import SignUpView, SignInView
import app_settings

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
jwt = JWTManager(app)
