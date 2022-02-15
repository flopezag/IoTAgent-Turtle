#export DOCKER_BUILDKIT=1
#docker build -t flask-application --cache-from flask-application --build-arg BUILDKIT_INLINE_CACHE=1 .
FROM  python:3.9-alpine  as  build
RUN  apk  update
# RUN apt-get install -y --no-install-recommends \
# 	build-essential gcc

WORKDIR  /usr/app
RUN  python  -m  venv  /usr/app/venv
ENV  PATH="/usr/app/venv/bin:$PATH"

COPY  requirements.txt  .
RUN  pip  install  -r  requirements.txt

FROM python:3.9-alpine@sha256:e80214a705236091ee3821a7e512e80bd3337b50a95392a36b9a40b8fc0ea183

RUN  addgroup  -g  99  python  &&  \
     adduser   -S  -u  999  -g  python  python

RUN  mkdir  /usr/app  &&  chown  python:python  /usr/app
WORKDIR  /usr/app

COPY  --chown=python:python  --from=build  /usr/app/venv  ./venv
COPY  --chown=python:python  .  .

USER 999

ENV PATH="/usr/app/venv/bin:$PATH"
CMD [ "python", "agent.py", "server"]
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl -f https://localhost:5000/version
