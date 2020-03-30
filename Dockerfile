FROM maestroserver/maestro-python-gcc

ENV APP_PATH=/opt/application
ENV PATH "$PATH:/home/app/.local/bin"
WORKDIR $APP_PATH

COPY ./app app/
COPY ./instance instance/
COPY requirements.txt requirements.txt
COPY package.json package.json
COPY run.py run.py
COPY docker-entrypoint.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/docker-entrypoint.sh
RUN addgroup app && adduser -S app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt


ENTRYPOINT ["/sbin/tini","-g","--"]
CMD ["docker-entrypoint.sh"]