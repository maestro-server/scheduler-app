FROM python:alpine3.6
MAINTAINER Felipe Signorini <felipe.signorini@maestroserver.io>

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

RUN apk add --no-cache --virtual .build-dependencies build-base tini su-exec curl-dev libressl-dev
RUN addgroup app && adduser -S app

ENV APP_PATH=/opt/application
ENV PATH "$PATH:/home/app/.local/bin"
WORKDIR $APP_PATH

COPY ./app $APP_PATH/app
COPY ./instance $APP_PATH/instance
COPY requirements.txt requirements.txt
COPY package.json package.json
COPY run.py run.py

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN apk del --no-cache --purge .build-deps \
RUN rm -rf /var/cache/apk/*

ENTRYPOINT ["/sbin/tini","-g","--"]
CMD ["docker-entrypoint.sh"]