from pydub import AudioSegment
from celery import Celery
import traceback
import os
import app_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from batch_model.model import Task, FileStatus, User, db
from gcpStorage import GCPStorage
from mail_send import MailSend
engine = create_engine(app_settings.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
connection = engine.connect()
celery_app = Celery(__name__, broker=app_settings.MESSAGE_QUEUE_URI)

  
            
           
            
@celery_app.task(name='convert_audio')  
def convert_audio():

    validTasks = 0
    errorTasks = 0
    pendingTasks = Task.query.filter(Task.status == FileStatus.UPLOADED).limit(500).all()

    for pendingTask in pendingTasks:
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
            validTasks = validTasks + 1
        print(message)
        if valid:
            try:
                GCPStorage.download_file(pendingTask.user + "/" + pendingTask.file, originFilePath)
                if extension == ".wav":
                    input = AudioSegment.from_wav(originFilePath)
                    input.export(targetFilePath, format=targetExtension)
                elif extension == ".mp3":
                    input = AudioSegment.from_mp3(originFilePath)
                    input.export(targetFilePath, format=targetExtension)
                elif extension == ".ogg":
                    input = AudioSegment.from_ogg(originFilePath)
                    input.export(targetFilePath, format=targetExtension)

                GCPStorage.upload_file(targetFilePath, pendingTask.user + "/" + fileName + "." + targetExtension)
                message = "El archivo ha sido descargado correctamente, podrá descargarlo con el nombre " + fileName + "." + targetExtension
                print(message)
                validTasks = validTasks + 1
            except Exception as e:
                traceback.print_exc()
                valid = False
                message = "No se pudo realizar la conversión porque se presentó un error durante la covnersión, revise el formato del archivo cargado. " + str(e) 
                errorTasks = errorTasks + 1
                print('Error al convertir el archivo: ' + message)
        pendingTask.status = FileStatus.PROCESSED if valid or "La conversión requerida ya había sido realizada, puede descargar el archivo" in message else FileStatus.ERROR

        session.commit()
        try:
            mailSender = MailSend()
            user = User.query.filter(User.username == pendingTask.user).first()
            subject = "Se ha terminado la conversión del archivo " + originFileName
            message = "<br/> Hemos terminado la conversión del archivo con el siguiente resultado:<br/> <br/> <br/> " + message
            mailSender.send_email(user.email, subject, message)
        except:
            print("No se pudo enviar el correo")

        return str(validTasks) + " Ok, " + str(errorTasks) + " con error"           
           