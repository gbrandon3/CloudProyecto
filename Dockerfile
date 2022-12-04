FROM python:3.7-slim-buster
WORKDIR /cloud

RUN apt-get -y update
RUN apt-get install -y ffmpeg
COPY requirements.txt requirements.txt
RUN  pip install -r requirements.txt
EXPOSE 5000

COPY . .
ENTRYPOINT ["gunicorn","--bind","0.0.0.0:5000","tasks:app"]

