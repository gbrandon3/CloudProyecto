import os
import sys
from datetime import datetime
import traceback
from flask import request
from flask_restful import Resource
from pydub import AudioSegment
from werkzeug.utils import secure_filename
import app_settings
from gcpStorage import GCPStorage
from mail_send import MailSend
from model import Task, TaskModelSchema, User, db
from model.taskModel import FileStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
taskSchema = TaskModelSchema()


class ConvertView(Resource):
    def delete(self):
        Task.query.delete()
        User.query.delete()
            