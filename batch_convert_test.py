from email import header
import json
from pydub import AudioSegment

import os
import app_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from batch_model.model import Task, FileStatus, User, db
from mail_send import MailSend
from wsgiref.simple_server import make_server


def convert(environ,start_response):
    method = environ['REQUEST_METHOD']
    if(method=="PUT"):
        engine = create_engine(app_settings.SQLALCHEMY_DATABASE_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        connection = engine.connect()

        pendingTask = session.query(Task).filter(Task.status == FileStatus.UPLOADED).first()
        
        if(pendingTask!=None):
        
            message = ""
            valid = True
            originFileName = pendingTask.file
            targetExtension = pendingTask.newExtension
            fileName, extension = os.path.splitext(originFileName)
            originFilePath = os.path.join(app_settings.RUTA_REPOSITORIO, pendingTask.user, originFileName)
            targetFilePath = os.path.join(app_settings.RUTA_REPOSITORIO, pendingTask.user, fileName + "." + targetExtension)
    
            if not targetExtension in app_settings.EXTENSIONES_PERMITIDAS:
                valid = False
                message = "La extensión del archivo a convertir no se encuentra dentro de las extensiones habilitadas"

            if not targetExtension in app_settings.EXTENSIONES_PERMITIDAS:
                valid = False
                message = "La extensión a la que desea convertir no se encuentra dentro de las extensiones habilitadas"

            if "." + targetExtension == extension:
                valid = False
                message = "La extensión a la que desea convertir es la misma del archivo orifinal y no se requiere realizar ninguna conversión"

            if valid and not os.path.exists(originFilePath):
                valid = False
                message = "El archivo de origen no se encontró"

            if valid and os.path.exists(targetFilePath):
                valid = False
                message = "La conversión requerida ya había sido realizada, puede descargar el archivo"

            if valid:
                try:
                    if extension == ".wav":
                        input = AudioSegment.from_wav(originFilePath)
                        input.export(targetFilePath, format=targetExtension)
                    elif extension == ".mp3":
                        input = AudioSegment.from_mp3(originFilePath)
                        input.export(targetFilePath, format=targetExtension)
                    elif extension == ".ogg":
                        input = AudioSegment.from_ogg(originFilePath)
                        input.export(targetFilePath, format=targetExtension)
                        message = "El archivo ha sudo descargado correctamente, podrá descargarlo con el nombre " + fileName + "." + targetExtension
                except:
                    valid = False
                    message = "No se pudo realizar la conversión porque se presentó un error durante la covnersión, revise el formato del archivo cargado."

            pendingTask.status = FileStatus.PROCESSED if valid else FileStatus.ERROR
            session.commit()
            mailSender = MailSend()
            user = session.query(User).filter(User.username == pendingTask.user).first()
            subject = "Se ha terminado la conversión del archivo " + originFileName
            message = "<br/> Hemos terminado la conversión del archivo con el siguiente resultado:<br/> <br/> <br/> " + message
            mailSender.send_email(user.email, subject, message)
            if(valid):
                headers=[('Content-type','application/json')]
                start_response('200 OK',headers)
                response={
                    "mensaje":message
            }
                return [bytes(json.dumps(response),'utf-8')]
            else:
                headers=[('Content-type','application/json')]
                start_response('400 ERROR',headers)
                response={
                    "mensaje":message}
                return [bytes(json.dumps(response),'utf-8')]
                
        else:
            headers=[('Content-type','application/json')]
            start_response('200 OK',headers)
            response={
                "mensaje":"No hay mas tareas"
         }
        
            return [bytes(json.dumps(response),'utf-8')]
    else:
        headers=[('Content-type','application/json')]
        start_response('404 ERROR',headers)
        response={
                "mensaje":"ENDPOINT NO VALIDO"
         }
        
        return [bytes(json.dumps(response),'utf-8')]

servidor=make_server('localhost',8000,convert)
servidor.serve_forever()

