FROM alpine/git as git-clone

ARG PROJECT=flopezag
ARG COMPONENT=IoTAgent-Turtle
ARG BRANCH=develop
ARG INSTALLATION_PATH=/opt/$COMPONENT

RUN mkdir -p $INSTALLATION_PATH
RUN git clone https://github.com/$PROJECT/$COMPONENT --branch $BRANCH $INSTALLATION_PATH


## Install PIP Requirements
FROM python:3.11-alpine as pip-requirements

ARG PROJECT=flopezag
ARG COMPONENT=IoTAgent-Turtle
ARG INSTALLATION_PATH=/opt/$COMPONENT

RUN mkdir -p $INSTALLATION_PATH
COPY --from=git-clone $INSTALLATION_PATH/requirements.txt /requirements.txt
RUN pip install --root-user-action=ignore --prefix=$INSTALLATION_PATH -r /requirements.txt


FROM python:3.11-alpine as final

LABEL "maintainer"="FIWARE Foundation e.V."
LABEL "description"="An Internet of Things Agent for the RDF DataQube Turtle format. This IoT Agent is designed to be a bridge between ISOXML/ADAPT and the ETSI NGSI-LD interface of a FIWARE Context Broker."
LABEL "name"="iotagent-turtle"
LABEL "summary"="IoT Agent for the DataQube representation in RDF Turtle format used in statistical environments"

LABEL "org.opencontainers.image.authors"="fernando.lopez@fiware.org"
LABEL "org.opencontainers.image.documentation"=""
LABEL "org.opencontainers.image.vendor"="FIWARE Foundation e.V."
LABEL "org.opencontainers.image.licenses"="Apache2.0"
LABEL "org.opencontainers.image.title"="iotagent-turtle"
LABEL "org.opencontainers.image.description"="An Internet of Things Agent for the RDF DataQube Turtle format. This IoT Agent is designed to be a bridge between ISOXML/ADAPT and the ETSI NGSI-LD interface of a FIWARE Context Broker."
LABEL "org.opencontainers.image.source"="https://github.com/flopezag/IoTAgent-Turtle"
LABEL "org.opencontainers.image.version"="0.1.0"
LABEL "org.python.version"="python:3.9"


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

