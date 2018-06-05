FROM python:alpine3.6
MAINTAINER Felipe Signorini <felipe.signorini@maestroserver.io>

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

RUN apk add --no-cache tini su-exec
RUN addgroup app && adduser -S app

ENV APP_PATH=/opt/application
WORKDIR $APP_PATH

COPY ./app $APP_PATH/app
COPY ./instance $APP_PATH/instance
COPY requirements.txt requirements.txt
COPY package.json package.json
COPY run.py run.py

ENV PATH "$PATH:/home/app/.local/bin"
RUN pip3 install -r requirements.txt

ENTRYPOINT ["/sbin/tini","-g","--"]
CMD ["docker-entrypoint.sh"]

