FROM python:alpine3.6
MAINTAINER Felipe Signorini <felipe.signorini@maestroserver.io>

ENV APP_PATH=/opt/application
WORKDIR $APP_PATH

COPY ./app $APP_PATH/app
COPY ./instance $APP_PATH/instance
COPY requirements.txt requirements.txt
COPY package.json package.json

RUN pip3 install -r requirements.txt

CMD celery -A app.celery worker -B -Q scheduler --loglevel=info
