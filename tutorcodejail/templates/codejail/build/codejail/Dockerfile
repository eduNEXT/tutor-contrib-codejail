FROM docker.io/ubuntu:22.04 AS minimal
LABEL mantainer="edunext.co <contact@edunext.co>"

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt install -y build-essential curl git language-pack-en llvm
ENV LC_ALL=en_US.UTF-8

###### Install python with pyenv in /opt/pyenv and create virtualenv in /openedx/venv
FROM minimal AS python
# https://github.com/pyenv/pyenv/wiki/Common-build-problems#prerequisites
RUN apt update && \
    apt install -y \
    curl \
    git \
    libbz2-dev \
    libffi-dev \
    liblzma-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    llvm \
    python3-openssl \
    subversion \
    tk-dev \
    wget \
    xz-utils \
    zlib1g-dev

ENV PYENV_ROOT=/opt/pyenv
RUN git clone \
    --branch v2.4.0 \
    --depth 1 https://github.com/pyenv/pyenv "$PYENV_ROOT"

ARG SANDBOX_PYTHON_VERSION="{{ CODEJAIL_SANDBOX_PYTHON_VERSION }}"
RUN git clone \
    https://github.com/esinker/pyenv-version-alias \
    "$PYENV_ROOT/plugins/pyenv-alias"

ARG CODEJAILSERVICE_PYTHON_VERSION=3.11.9
RUN "$PYENV_ROOT/bin/pyenv" install "$CODEJAILSERVICE_PYTHON_VERSION"

RUN VERSION_ALIAS="{{ CODEJAIL_SANDBOX_PYTHON_VERSION }}_sandbox" \
    "$PYENV_ROOT/bin/pyenv" install -f "$SANDBOX_PYTHON_VERSION"

RUN "$PYENV_ROOT/versions/$CODEJAILSERVICE_PYTHON_VERSION/bin/python" -m venv /openedx/venv
RUN "$PYENV_ROOT/versions/"$SANDBOX_PYTHON_VERSION"_sandbox/bin/python" -m venv --copies /sandbox/venv

###### Codejail service code
FROM minimal AS code
RUN git clone \
    --branch '{{ CODEJAIL_SERVICE_VERSION }}' \
    --depth 1 \
    "{{ CODEJAIL_SERVICE_REPOSITORY }}"\
    /openedx/codejailservice

WORKDIR /openedx/codejailservice

###### Install python requirements in virtualenv
FROM python AS codejailservice-python-requirements

ENV PATH="/openedx/venv/bin:${PATH}"
ENV VIRTUAL_ENV=/openedx/venv/

COPY --from=code /openedx/codejailservice /openedx/codejailservice
WORKDIR /openedx/codejailservice
RUN pip3 install -r requirements/base.txt
RUN pip3 install uwsgi==2.0.21

###### Install python requirements in virtualenv
FROM python AS sandbox-python-requirements

ARG EDX_PLATFORM_REPOSITORY="{{ EDX_PLATFORM_REPOSITORY }}"
ARG EDX_PLATFORM_VERSION="{{ EDX_PLATFORM_VERSION }}"

ENV PATH="/sandbox/venv/bin:${PATH}"
ENV VIRTUAL_ENV=/sandbox/venv/

WORKDIR /var/tmp
RUN mkdir -p common/lib/

ADD $EDX_PLATFORM_REPOSITORY#$EDX_PLATFORM_VERSION:requirements/edx-sandbox/releases .
RUN pip3 install -r sumac.txt

# Allows you to add extra pip requirements to your codejail sandbox.
{% if CODEJAIL_EXTRA_PIP_REQUIREMENTS is defined %}
{% for extra_requirements in CODEJAIL_EXTRA_PIP_REQUIREMENTS %}RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install '{{ extra_requirements }}'
{% endfor %}
{% endif %}

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

ENV PATH=/openedx/venv/bin:${PATH}
ENV VIRTUAL_ENV=/openedx/venv/
WORKDIR /openedx/codejailservice

EXPOSE 8550
CMD uwsgi \
    --http 0.0.0.0:8550 \
    --thunder-lock \
    --single-interpreter \
    --enable-threads \
    --processes=${UWSGI_WORKERS:-2} \
    --buffer-size=8192 \
    --max-requests=1000 \
    --wsgi-file /openedx/codejailservice/wsgi.py
