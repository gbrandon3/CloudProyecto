# CloudProyecto


El proyecto se debe correr en una maquina linux para hacer la conversion de audio

Instalar las librerias usadas


    pip install -r requirements.txt

##  Instalación de la librería de conversión de audio (pudyb + ffmpeg )
Instalar ffmpeg

    apt-get install ffmpeg libavcodec-extra

Se debe crear el directorio de repositorio en donde se almacenan los archivos a convertir y los convertidos

    sudo mkdir /RepositorioMISO/

Dependiendo de la configuración del servidor WEB se podrían requerir permisos de escritura y eliminación en tal directorio para el usuario que ejecuta el servidor WEB, 
se pueden dar permisos genéricos  así:

    sudo chmod -R 777 /RepositorioMISO/

Para ejecutar en shell el script de conversión, el archivo debe tener permisos de ejecución

    chmod 755 batch_conversion/convertir_audio.py

Para correr el script en pruebas, se ejecuta el siguiente comando desde la carpeta raiz del proyecto

    python3 batch_conversion.py 

##  Configuración (app_settings.py)

El archivo /app_settings.py contiene las siguientes variables de configuración, ajústelas acorde a sus parámetros locales de instalación:

```
SQLALCHEMY_DATABASE_URI: URI de la base de datos postgres
RUTA_REPOSITORIO: Directorio base donde se almacenan los archivos cargados y procesados
MESSAGE_QUEUE_URI= Uri del servidor de rabbitmq


```
Para la ejecucion 
aplicacion flask run
En la carpeta del la aplicacion

Para la ejecucion de la cola de tareas  de pub/sub se debe crear un servicio en gcp, generar una cuenta de acceso y crear un archivo para los permisos, modificar las variables PUBLISHER_PATH por el topic SUB_PATH por la subscripcion y  UTH_PUB_SUB por el archvio descargado que contiene los permisos, luego ejecutar el script tasks.py

