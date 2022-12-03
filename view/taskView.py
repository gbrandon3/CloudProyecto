import os
import sys
from datetime import datetime
from gcpStorage import GCPStorage
from flask import request, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from werkzeug.utils import secure_filename
from werkzeug import Response
from google.cloud import pubsub_v1
from model import db, User, Task, TaskModelSchema
from model.taskModel import FileStatus
import app_settings
crepential_path= os.getcwd()+"/"+app_settings.AUTH_PUB_SUB

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = crepential_path
taskSchema = TaskModelSchema()

class TaskView( Resource):
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
        
                task.delete()
                db.session.commit()
            
                return "Tarea eliminada correctamente",200
            else:
                return "Tarea no encontrada",400
        else:
            return "Usuario no encontrado", 404
    @jwt_required()
    def put(self,id_task):
        if request . json["newFormat"] not in app_settings . EXTENSIONES_PERMITIDAS :
            return "Extension no permitida",400
        identity = get_jwt_identity()
        user = User.query.get_or_404(identity)   
        if user is not None:
            task=Task.query.filter(Task.id == id_task).first()
            if task is not None:
                if(task.status!= FileStatus.UPLOADED):
                    ruta=os.path.join(app_settings.RUTA_REPOSITORIO,user.username)
                    archivo=task.file.split(".")[0]+"."+task.newExtension
                    if os.path.exists(os.path.join(ruta,archivo)):
                        os.remove(os.path.join(os.path.join(ruta,archivo)))
                        
               
                task.newExtension=request.json["newFormat"]
                task.status=FileStatus.UPLOADED
                db.session.commit()
                return taskSchema.dump(task)           
            else:
                return "Tarea no encontrada",400   
            
   



class TasksView(Resource):

    @jwt_required()
    def post(self):
        identity=get_jwt_identity()
        user=User.query.get_or_404(identity)
        if(user!=None):
          
            fileUploaded=request.files["fileName"]
       
            fileName=secure_filename(fileUploaded.filename)
            if(fileName.split(".")[1]in app_settings.EXTENSIONES_PERMITIDAS):
                task=Task( timestmap=datetime.now(),file=fileName,newExtension=request.values.get('newFormat'),status=FileStatus.UPLOADED)
                user.tasks.append(task)
                db.session.commit()
                try:
                    rutaArchivo = user.username + "/" + fileName
                    GCPStorage.upload_blob(fileUploaded.stream, rutaArchivo)
                except Exception as e: 
                    return "No se pudo guardar el archivo " + str(e),500
                try:
                    publisher = pubsub_v1.PublisherClient()
                    topic_path = app_settings.PUBLISHER_PATH
                    attr={'taskId':str(task.id)}
                    data="Convertir"
                    data = data.encode('utf-8')
                    publisher.publish(topic_path, data,**attr)   
                except Exception as e:
                    return 'Error: al publicar la tarea error'+ str(e),400
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
            rutaArchivo = user.username + "/" + file_name
            contenido = GCPStorage.download_blob(rutaArchivo)
            mimetype="audio/wav"
            if file_name.endswith(".mp3"):
                mimetype = "audio/mpeg"
            if file_name.endswith(".ogg"):
                mimetype = "audio/ogg"
            return Response(contenido, mimetype=mimetype)
        else:
            return "Usuario no encontrado", 404