FROM docker.io/python:3.11-slim

USER root

RUN apt-get -y update
RUN apt-get install -y sqlite3 libsqlite3-dev
RUN python3 -m pip install flask markdown requests

RUN mkdir /app
ENV AP /app
RUN mkdir $AP/volumes
RUN mkdir $AP/templates
RUN mkdir $AP/static
ENV PORT 8080

RUN useradd -m -d $AP agora
# USER agora

COPY ./src/server.py $AP/
COPY ./src/utilities/ $AP/utilities/
COPY ./src/params/ $AP/params/

WORKDIR $AP

CMD ["sh", "-c", "python3 server.py ${PORT} \"${MAILGUN_KEY}\" ${HOST} ${RECAPTCHA_SITEKEY} ${RECAPTCHA_SERVERKEY} \"${DEV_EMAILS}\""]

