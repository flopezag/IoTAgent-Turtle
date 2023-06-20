FROM alpine/git as git-clone

ARG PROJECT=flopezag
ARG COMPONENT=IoTAgent-Turtle
ARG VERSION=develop
ARG INSTALLATION_PATH=/opt/$COMPONENT

RUN mkdir -p $INSTALLATION_PATH
RUN git clone https://github.com/$PROJECT/$COMPONENT --branch $VERSION $INSTALLATION_PATH


## Install PIP Requirements
FROM python:3.11-alpine as pip-requirements

ARG PROJECT=flopezag
ARG COMPONENT=IoTAgent-Turtle
ARG VERSION=integration-cb-httpserver
ARG INSTALLATION_PATH=/opt/$COMPONENT

RUN mkdir -p $INSTALLATION_PATH
COPY --from=git-clone $INSTALLATION_PATH/requirements.txt /requirements.txt
RUN pip install --root-user-action=ignore --prefix=$INSTALLATION_PATH -r /requirements.txt


FROM python:3.11-alpine as final

ARG PROJECT=flopezag
ARG COMPONENT=IoTAgent-Turtle
ARG INSTALLATION_PATH=/opt/$COMPONENT

ENV PORT=${IOTA_PORT:-5000}

RUN mkdir -p $INSTALLATION_PATH

COPY --from=git-clone $INSTALLATION_PATH $INSTALLATION_PATH
COPY --from=pip-requirements $INSTALLATION_PATH /usr/local

COPY config.json $INSTALLATION_PATH/common/config.json
WORKDIR $INSTALLATION_PATH

EXPOSE ${PORT}
ENTRYPOINT /usr/local/bin/python agent.py server --host 0.0.0.0 --port ${PORT}

expose $PORT
