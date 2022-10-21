FROM python:3.7-alpine
WORKDIR /cloud

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0


RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk add postgresql-dev gcc python3-dev musl-dev
COPY requirements.txt requirements.txt
RUN  pip install -r requirements.txt

EXPOSE 5000
COPY . .
CMD ["flask", "run"]