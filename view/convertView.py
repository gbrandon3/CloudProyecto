import os
import sys
from datetime import datetime

from flask_restful import Resource
from pydub import AudioSegment

from model import db, User, Task, TaskModelSchema
from model.taskModel import FileStatus
from mail_send import MailSend

import app_settings

taskSchema = TaskModelSchema()


class ConvertView(Resource):
    def get(self):
        pendingTasks = Task.query.filter(Task.status == FileStatus.UPLOADED).limit(5).all()
        validTasks = 0
        errorTasks = 0
        for pendingTask in pendingTasks:
            print(pendingTask)
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
                    validTasks = validTasks + 1
                except:
                    valid = False
                    message = "No se pudo realizar la conversión porque se presentó un error durante la covnersión, revise el formato del archivo cargado."
                    errorTasks = errorTasks + 1

            pendingTask.status = FileStatus.PROCESSED if valid else FileStatus.ERROR
            db.session.commit()
            mailSender = MailSend()
            user = User.query.filter(User.username == pendingTask.user).first()
            subject = "Se ha terminado la conversión del archivo " + originFileName
            message = "<br/> Hemos terminado la conversión del archivo con el siguiente resultado:<br/> <br/> <br/> " + message
            mailSender.send_email(user.email, subject, message)

        return validTasks + " Ok, " + errorTasks + " con error"           

