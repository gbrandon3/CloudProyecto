from pydub import AudioSegment

import os
import app_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from batch_model.model import Task, FileStatus, db


engine = create_engine(app_settings.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
connection = engine.connect()

pendingTasks = session.query(Task).filter(Task.status == FileStatus.UPLOADED)

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
        except:
            valid = False
            message = "No se pudo realizar la conversión porque se presentó un error durante la covnersión, revise el formato del archivo cargado."

    pendingTask.status = FileStatus.UPLOADED if valid else FileStatus.ERROR
    session.commit()

