import os 
from google.cloud import pubsub_v1
from pydub import AudioSegment
from celery import Celery

import os
import app_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from batch_model.model import Task, FileStatus, User, db
from mail_send import MailSend
crepential_path= os.getcwd()+"/"+"miso-4cloud-769393b6b084.json"
print(crepential_path)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = crepential_path
engine = create_engine(app_settings.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
connection = engine.connect()

subscriber=pubsub_v1.SubscriberClient()
sub_path='projects/miso-4cloud/subscriptions/convert-sub'

def convert_audio(messagepub):

    validTasks = 0
    errorTasks = 0
    pendingTask = session.query(Task).filter(Task.status == FileStatus.UPLOADED,).order_by(Task.id.desc()).first()
    if(pendingTask!=None):
        print(pendingTask.id)   
    print(messagepub)
    print(messagepub.data)
      
    
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
            validTasks = validTasks + 1
       
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
                print("AQUI")
                valid = False
                message = "No se pudo realizar la conversión porque se presentó un error durante la covnersión, revise el formato del archivo cargado."
                errorTasks = errorTasks + 1
        pendingTask.status = FileStatus.PROCESSED if valid or "La conversión requerida ya había sido realizada, puede descargar el archivo" in message else FileStatus.ERROR
        session.commit()
        try:
            mailSender = MailSend()
            user = session.query(User).filter(User.username == pendingTask.user).first()
            subject = "Se ha terminado la conversión del archivo " + originFileName
            message = "<br/> Hemos terminado la conversión del archivo con el siguiente resultado:<br/> <br/> <br/> " + message
            mailSender.send_email(user.email, subject, message)
        except Exception as e :
            print("No se pudo enviar el correo"+str(e))

        print(str(validTasks) + " Ok, " + str(errorTasks) + " con error"   )
        messagepub.ack()    
streaming_pull_future=subscriber.subscribe(sub_path,callback=convert_audio)

with subscriber:
    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
