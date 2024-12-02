FROM docker.io/ubuntu:22.04 AS minimal
LABEL mantainer="edunext.co <contact@edunext.co>"

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt install -y \
        build-essential \
        git \
        language-pack-en
ENV LC_ALL=en_US.UTF-8

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
    xz-utils \
    zlib1g-dev

ENV PYENV_ROOT=/opt/pyenv
ADD https://github.com/pyenv/pyenv.git#v2.4.0 "$PYENV_ROOT"
ADD https://github.com/esinker/pyenv-version-alias.git "$PYENV_ROOT/plugins/pyenv-alias"

ARG CODEJAILSERVICE_PYTHON_VERSION=3.11.9
RUN "$PYENV_ROOT/bin/pyenv" install "$CODEJAILSERVICE_PYTHON_VERSION"

ARG SANDBOX_PYTHON_VERSION="{{ CODEJAIL_SANDBOX_PYTHON_VERSION }}"
RUN VERSION_ALIAS="{{ CODEJAIL_SANDBOX_PYTHON_VERSION }}_sandbox" \
    "$PYENV_ROOT/bin/pyenv" install -f "$SANDBOX_PYTHON_VERSION"

RUN "$PYENV_ROOT/versions/$CODEJAILSERVICE_PYTHON_VERSION/bin/python" -m venv --copies /openedx/venv
RUN "$PYENV_ROOT/versions/"$SANDBOX_PYTHON_VERSION"_sandbox/bin/python" -m venv --copies /sandbox/venv

# Codejail service code
FROM scratch AS codejail-code
ADD --keep-git-dir=true "{{ CODEJAIL_SERVICE_REPOSITORY }}#{{ CODEJAIL_SERVICE_VERSION }}" .

FROM minimal AS codejail-requirements
COPY --from=python /opt/pyenv /opt/pyenv
COPY --from=python /openedx/venv /openedx/venv

WORKDIR /temp
ENV PATH="/openedx/venv/bin:${PATH}"
ENV VIRTUAL_ENV=/openedx/venv/
COPY --from=codejail-code /requirements/base.txt .
RUN pip install -r base.txt uwsgi==2.0.21

FROM minimal AS sandbox-requirements
COPY --from=python /opt/pyenv /opt/pyenv
COPY --from=python /sandbox/venv /sandbox/venv

WORKDIR /temp
ENV PATH="/sandbox/venv/bin:${PATH}"
ENV VIRTUAL_ENV=/sandbox/venv/

ARG EDX_PLATFORM_REPOSITORY="{{ EDX_PLATFORM_REPOSITORY }}"
ARG EDX_PLATFORM_VERSION="{{ EDX_PLATFORM_VERSION }}"
ADD $EDX_PLATFORM_REPOSITORY#$EDX_PLATFORM_VERSION:requirements/edx-sandbox/releases .
RUN pip3 install -r sumac.txt

# Allows you to add extra pip requirements to your codejail sandbox.
{% if CODEJAIL_EXTRA_PIP_REQUIREMENTS is defined %}
{% for extra_requirements in CODEJAIL_EXTRA_PIP_REQUIREMENTS %}
RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install '{{ extra_requirements }}'
{% endfor %}
{% endif %}

FROM minimal AS production
RUN apt update && \
    apt install -y sudo

COPY --from=python /opt/pyenv /opt/pyenv
COPY --from=codejail-code / /openedx/codejailservice
COPY --from=sandbox-requirements /sandbox/venv /sandbox/venv
COPY --from=codejail-requirements /openedx/venv /openedx/venv
ENV PATH="/openedx/venv/bin:${PATH}"
ENV VIRTUAL_ENV=/openedx/venv/

# Setup sandbox
ENV SANDBOX_ENV=/sandbox/venv
RUN groupadd -r sandbox && useradd -m -r -g sandbox sandbox && chown -R sandbox:sandbox /sandbox

ENV PATH=/openedx/venv/bin:${PATH}
ENV VIRTUAL_ENV=/openedx/venv/
WORKDIR /openedx/codejailservice

EXPOSE 8550

CMD [ "uwsgi" , \
    "--http=0.0.0.0:8550", \
    "--thunder-lock", \
    "--single-interpreter", \
    "--enable-threads", \
    "--processes=2", \
    "--buffer-size=8192", \
    "--max-requests=1000", \
    "--wsgi-file=/openedx/codejailservice/wsgi.py" ]
