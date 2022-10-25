# CloudProyecto

##  Instalación de la librería de conversión de audio (pudyb + ffmpeg )

Instalar la versión v0.25.1 de pydub


    pip install -r requirements.txt

Las instrucciones detalladas están disponibles en https://github.com/jiaaro/pydub#installation


Luego instalar ffmpeg

    apt-get install ffmpeg libavcodec-extra

Se debe crear el directorio de repositorio en donde se almacenan los archivos a convertir y los convertidos

    sudo mkdir /RepositorioMISO/

Dependiendo de la configuración del servidor WEB se podrían requerir permisos de escritura y eliminación en tal directorio para el usuario que ejecuta el servidor WEB, 
se pueden dar permisos genéricos  así:

    sudo chmod -R 777 /RepositorioMISO/

Para ejecutar en shell el script de conversión, el archivo debe tener permisos de ejecución

    chmod 755 batch_conversion/convertir_audio.py

Para correr el script en pruebas, se ejecuta el siguiente comando desde la carpeta raiz del proyecto

    python3 batch_conversion/convertir_audio.py 

##  Configuración (app_settings.py)

El archivo /app_settings.py contiene las siguientes variables de configuración, ajústelas acorde a sus parámetros locales de instalación:

```
SQLALCHEMY_DATABASE_URI: URI de la base de datos postgres
RUTA_REPOSITORIO: Directorio base donde se almacenan los archivos cargados y procesados
EXTENSIONES_PERMITIDAS: Array con las extensiones permitidas para cargar, sin punto

```
