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
    apt install -y libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git subversion
ENV PYENV_ROOT=/opt/pyenv
RUN git clone https://github.com/pyenv/pyenv $PYENV_ROOT --branch v2.6.12 --depth 1

ARG CODEJAILSERVICE_PYTHON_VERSION=3.11.14
RUN $PYENV_ROOT/bin/pyenv install $CODEJAILSERVICE_PYTHON_VERSION

ARG SANDBOX_PYTHON_VERSION="{{ CODEJAIL_SANDBOX_PYTHON_VERSION }}"
RUN git clone https://github.com/esinker/pyenv-version-alias $PYENV_ROOT/plugins/pyenv-alias
RUN VERSION_ALIAS="{{ CODEJAIL_SANDBOX_PYTHON_VERSION }}_sandbox" \
    $PYENV_ROOT/bin/pyenv install -f $SANDBOX_PYTHON_VERSION

RUN "$PYENV_ROOT/versions/$CODEJAILSERVICE_PYTHON_VERSION/bin/python" -m venv /openedx/venv
RUN "$PYENV_ROOT/versions/"$SANDBOX_PYTHON_VERSION"_sandbox/bin/python" -m venv --copies /sandbox/venv

###### Codejail service code
FROM minimal AS code
RUN git clone {{ CODEJAIL_SERVICE_REPOSITORY }} --branch {{ CODEJAIL_SERVICE_VERSION }} --depth 1 /openedx/codejailservice
WORKDIR /openedx/codejailservice

###### Install python requirements in virtualenv
FROM python AS codejailservice-python-requirements

ENV PATH=/openedx/venv/bin:${PATH}
ENV VIRTUAL_ENV=/openedx/venv/

COPY --from=code /openedx/codejailservice /openedx/codejailservice
WORKDIR /openedx/codejailservice
RUN pip3 install -r requirements/base.txt
RUN pip3 install uwsgi==2.0.21

###### Install python requirements in virtualenv
FROM python AS sandbox-python-requirements

ARG EDX_PLATFORM_REPOSITORY={{ EDX_PLATFORM_REPOSITORY }}
ARG EDX_PLATFORM_VERSION={{ EDX_PLATFORM_VERSION }}

ENV PATH=/sandbox/venv/bin:${PATH}
ENV VIRTUAL_ENV=/sandbox/venv/

WORKDIR /var/tmp
RUN mkdir -p common/lib/

ADD $EDX_PLATFORM_REPOSITORY#$EDX_PLATFORM_VERSION:requirements/edx-sandbox/ .
RUN pip3 install -r base.txt

{% if CODEJAIL_EXTRA_PIP_REQUIREMENTS %}
# Allows you to add extra pip requirements to your codejail sandbox.
RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install \
{%- for extra_requirements in CODEJAIL_EXTRA_PIP_REQUIREMENTS %}
  '{{ extra_requirements }}' \
{%- endfor %}
;
{% endif %}

##### Prod image
FROM minimal AS production

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
ENV UWSGI_WORKERS=2
WORKDIR /openedx/codejailservice

EXPOSE 8550

CMD [ "uwsgi", \
    "--http=0.0.0.0:8550", \
    "--thunder-lock", \
    "--single-interpreter", \
    "--enable-threads", \
    "--buffer-size=8192", \
    "--max-requests=1000", \
    "--wsgi-file=/openedx/codejailservice/wsgi.py" ]
