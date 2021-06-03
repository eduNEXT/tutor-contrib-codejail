FROM docker.io/ubuntu:20.04 as minimal
MAINTAINER Overhang.io <contact@overhang.io>

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt install -y build-essential curl git language-pack-en
ENV LC_ALL en_US.UTF-8

###### Install python with pyenv in /opt/pyenv and create virtualenv in /openedx/venv
FROM minimal as python
# https://github.com/pyenv/pyenv/wiki/Common-build-problems#prerequisites
RUN apt update && \
    apt install -y libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git subversion
ENV PYENV_ROOT /opt/pyenv
RUN git clone https://github.com/pyenv/pyenv $PYENV_ROOT --branch v1.2.21 --depth 1

ARG CODEJAILSERVICE_PYTHON_VERSION=3.8.6
RUN $PYENV_ROOT/bin/pyenv install $CODEJAILSERVICE_PYTHON_VERSION

ARG SANDBOX_PYTHON_VERSION={{ SANDBOX_PYTHON_VERSION }}
RUN $PYENV_ROOT/bin/pyenv install $SANDBOX_PYTHON_VERSION

RUN $PYENV_ROOT/versions/$CODEJAILSERVICE_PYTHON_VERSION/bin/python -m venv /openedx/venv
RUN $PYENV_ROOT/versions/$SANDBOX_PYTHON_VERSION/bin/python -m venv --copies /sandbox/venv

###### Codejail service code
FROM minimal as code
RUN git clone https://github.com/eduNEXT/codejailservice.git --branch {{ CODEJAIL_VERSION }} --depth 1 /openedx/codejailservice
WORKDIR /openedx/codejailservice

###### Install python requirements in virtualenv
FROM python as codejailservice-python-requirements

ENV PATH /openedx/venv/bin:${PATH}
ENV VIRTUAL_ENV /openedx/venv/

COPY --from=code /openedx/codejailservice /openedx/codejailservice
WORKDIR /openedx/codejailservice
RUN pip3 install -r requirements/base.txt
RUN pip3 install ipdb

###### Install python requirements in virtualenv
FROM python as sandbox-python-requirements

ENV PATH /sandbox/venv/bin:${PATH}
ENV VIRTUAL_ENV /sandbox/venv/

WORKDIR /var/tmp
RUN mkdir -p common/lib/

COPY --from={{ DOCKER_IMAGE_OPENEDX }} /openedx/edx-platform/common/lib/sandbox-packages common/lib/sandbox-packages
COPY --from={{ DOCKER_IMAGE_OPENEDX }} /openedx/edx-platform/common/lib/sandbox-packages common/lib/symmath
COPY --from={{ DOCKER_IMAGE_OPENEDX }} /openedx/edx-platform/requirements/edx-sandbox/py35.txt py35.txt
RUN pip3 install -r py35.txt

##### Prod image
FROM minimal as production

# Install system requirements
RUN apt update && \
    apt install -y sudo

COPY --from=code /openedx/codejailservice /openedx/codejailservice
COPY --from=python /opt/pyenv /opt/pyenv
COPY --from=codejailservice-python-requirements /openedx/venv /openedx/venv
COPY --from=sandbox-python-requirements /sandbox/venv /sandbox/venv

# Setup sandbox
ENV SANDBOX_ENV=/sandbox/venv
RUN groupadd -r sandbox && useradd -m -r -g sandbox sandbox && chown -R sandbox:sandbox /sandbox

ENV PATH /openedx/venv/bin:${PATH}
ENV VIRTUAL_ENV /openedx/venv/
WORKDIR /openedx/codejailservice

EXPOSE 8000
CMD gunicorn --workers=2 --name codejailservice --bind=0.0.0.0:8000 --max-requests=1000 codejailservice.wsgi:application