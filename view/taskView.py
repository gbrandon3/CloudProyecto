import os
import sys
from datetime import datetime

from flask import request, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from werkzeug.utils import secure_filename

from model import db, User, Task, TaskModelSchema
from model.taskModel import FileStatus
import app_settings

taskSchema = TaskModelSchema()


class TaskView(Resource):
    @jwt_required()
    def get(self, id_task):
        return taskSchema.dump(Task.query.get_or_404(id_task))

    @jwt_required()
    def delete(self, id_task):
        identity = get_jwt_identity()
        user = User.query.get_or_404(identity)
        if user is not None:
            task=Task.query.filter(Task.id == id_task)

            if(task.first()!=None):
        
                task.delete();
                db.session.commit()
            
                return "Tarea eliminada correctamente",200
            else:
                return "Tarea no encontrada",400
        else:
            return "Usuario no encontrado", 404


class TasksView(Resource):

    @jwt_required()
    def post(self):
        identity=get_jwt_identity()
        user=User.query.get_or_404(identity)
        if(user!=None):
          
            fileUploaded=request.files["fileName"]
       
            fileName=secure_filename(fileUploaded.filename)
            if(fileName.split(".")[1]in app_settings.EXTENSIONES_PERMITIDAS):
                user.tasks.append(Task( timestmap=datetime.now(),file=fileName,newExtension=request.values.get('newFormat'),status=FileStatus.UPLOADED))
                db.session.commit()
                try:
                    rutaUsuario = os.path.join(app_settings.RUTA_REPOSITORIO, user.username)
                    if not os.path.exists(rutaUsuario):
                        os.mkdir(rutaUsuario)
                    fileUploaded.save(os.path.join(rutaUsuario, fileName))
                except: 
                    return "No se pudo guardar el archivo",500
                return "Se ha creado la tarea exitosamente"
            else:
                return "Archivo no valido"
        else:
            return "Usuario no encontrado", 404

    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        user = User.query.get_or_404(identity)
        if user != None:
            order = request.json["order"]
            try:
                cantMax = request.json["max"]
                tasks = Task.query.filter(Task.user == identity).order_by(
                    Task.id.desc() if order == 1 else Task.id.asc()).limit(cantMax)
                return [taskSchema.dump(task) for task in tasks]
            except KeyError:
                tasks = [taskSchema.dump(task) for task in Task.query.filter(Task.user == identity).order_by(
                    Task.id.desc() if order == 1 else Task.id.asc()).all()]
                return tasks


        else:
            return "Usuario no encontrado", 404


class TaskViewFile(Resource):

    @jwt_required()
    def get(self, file_name):
        identity = get_jwt_identity()
        user = User.query.get_or_404(identity)
        if user is not None:
            task = Task.query.filter(Task.user == user.username, Task.file == file_name).first()
            print(task.status, file=sys.stderr)
            print("Ruta:" + os.getcwd(), file=sys.stderr)
            root = os.getcwd()
            path = '/uploads/uploaded/' if task.status == FileStatus.UPLOADED else '/process/process/'
            print("llego:", file=sys.stderr)
            return send_from_directory(root + path, file_name, as_attachment=True)
        else:
            return "Usuario no encontrado", 404