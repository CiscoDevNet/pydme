# By default - docker build will pull master
# If you want the local WS to be used - please use
# "--build-arg ." to the docker build command - like:
#
# 'docker build -t mypydme:latest --build-arg PYDME_SOURCE=. .
# You can only specify '.' as PYDME_SOURCE
#

FROM python:3.7-alpine
# TODO
ARG PYDME_SOURCE=https://github.com/CiscoDevNet/pydme/blob/master/archive/pydme.zip?raw=true

RUN apk add --update build-base
RUN apk add --update libffi-dev libxml2-dev libxslt-dev openssl openssl-dev
RUN apk add --update --no-cache bash git openssh && pip install anytree

WORKDIR /localws

RUN git clone https://github.com/CiscoDevNet/pydme.git

#hadolint ignore=DL3013
RUN pip install -U pip
COPY . $WORKDIR
#hadolint ignore=DL3013
RUN pip install $PYDME_SOURCE

