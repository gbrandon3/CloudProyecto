
from datetime import datetime

from sqlite3 import IntegrityError
from xmlrpc.client import DateTime
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from flask import request
from model import db,User,Task,TaskModelSchema
from flask import request
from flask_restful import Resource
from werkzeug.utils import secure_filename

from model.taskModel import FileStatus
taskSchema=TaskModelSchema()
class TaskView(Resource):
    @jwt_required()
    def get(self,id_task):
        return taskSchema.dump(Task.query.get_or_404(id_task))
class TasksView(Resource):
    extensionAllowed=["mp3","wav", "acc" ,"ogg", "wmaw"]
    @jwt_required()
    def post(self):
        identity=get_jwt_identity()
        user=User.query.get_or_404(identity)
        if(user!=None):
        
            fileUploaded=request.files["fileName"]
       
            fileName=secure_filename(fileUploaded.filename)
     
            user.tasks.append(Task( timestmap=datetime.now(),file=fileName,newExtension=request.values.get('newFormat'),status=FileStatus.UPLOADED))
            db.session.commit()
            try:
                fileUploaded.save(os.path.join("uploads/uploaded", fileName))
            except: 
                return "No se pudo guardar el archivo",500
            return "Se ha creado la tarea exitosamente"
        else:
            return "Usuario no encontrado",404

       
    @jwt_required()    
    def get(self):
        identity=get_jwt_identity()
        user=User.query.get_or_404(identity)
        if user!= None:
            order=request.json["order"]
            try:
                cantMax=request.json["max"]
                tasks=Task.query.filter(Task.user==identity).order_by(Task.id.desc() if order==1 else Task.id.asc()).limit(cantMax)
                return [taskSchema.dump(task) for task in tasks]
            except KeyError:
                tasks=[ taskSchema.dump(task) for task in  Task.query.filter(Task.user==identity).order_by(Task.id.desc() if order==1 else Task.id.asc()).all()]
                return tasks
            
                 
        else:
            return "Usuario no encontrado",404
 