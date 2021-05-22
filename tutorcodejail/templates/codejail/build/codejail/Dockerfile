FROM docker.io/ubuntu:20.04
MAINTAINER eduNEXT <contact@edunext.co>

RUN apt update && \
  apt upgrade -y && \
  # python 3.8
  apt install -y language-pack-en git python3 python3-pip libmysqlclient-dev
RUN ln -s /usr/bin/python3 /usr/bin/python \
    && ln -s /usr/bin/pip3 /usr/bin/pip


RUN mkdir /openedx
RUN git clone https://github.com/eduNEXT/codejailservice.git --branch eric/mvp --depth 1 /openedx/codejailservice
WORKDIR /openedx/codejailservice

RUN pip3 install -r requirements/base.txt

EXPOSE 8000
CMD gunicorn --workers=2 --name codejailservice --bind=0.0.0.0:8000 --max-requests=1000 codejailservice.wsgi:application
