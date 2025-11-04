FROM scratch AS codejail-service-code
ARG CODEJAIL_SERVICE_REPO={{ CODEJAIL_SERVICE_V2_REPOSITORY }}
ARG CODEJAIL_SERVICE_VERSION={{ CODEJAIL_SERVICE_V2_VERSION }}
ADD ${CODEJAIL_SERVICE_REPO}#${CODEJAIL_SERVICE_VERSION} /

FROM scratch AS sandbox-dependencies
# Where to get the Python dependencies lockfile for installing
# packages into the sandbox environment. Defaults to the codejail
# dependencies in edx-platform.
ARG SANDBOX_DEPS_REPO={{ EDX_PLATFORM_REPOSITORY }}
ARG SANDBOX_DEPS_VERSION={{ CODEJAIL_SERVICE_V2_VERSION }}
# Path to the lockfile in the deps repo, as dir + filename.
#
# The path base.txt will get the latest dependencies, but this needs
# to be coordinated with SANDBOX_PY_VER as each release has a
# different Python support window.
ARG SANDBOX_DEPS_SRC_DIR=requirements/edx-sandbox
ADD ${SANDBOX_DEPS_REPO}#${SANDBOX_DEPS_VERSION}:${SANDBOX_DEPS_SRC_DIR} /

FROM docker.io/ubuntu:24.04 AS app
ARG APP_PY_VER=3.12
# See codejail-service deployment and configuration docs for why we need to select
# a UID/GID that is unlikely to collide with anything on the host. (Short answer:
# RLIMIT_NPROC UID-global usage pool, and Docker not isolating UIDs.)
#
# Selected via: python3 -c 'import random; print(random.randrange(3000, 2 ** 31))'
ARG APP_UID=15826504
ARG APP_GID=$APP_UID

ARG SANDBOX_DEPS_SRC_FILE=base.txt

# Python version for sandboxed executions. This must be coordinated with
# `SANDBOX_DEPS_SRC_*` to ensure compatibility.
ARG SANDBOX_PY_VER={{ '.'.join(CODEJAIL_SANDBOX_PYTHON_VERSION.split('.')[:2]) }}


##### Base app installation #####

ENV DEBIAN_FRONTEND=noninteractive
ARG APT_INSTALL="apt-get install --quiet --yes --no-install-recommends"

# The codejail library specifies a certain structure to how the sandboxing is
# performed. (See the documentation in the codejail library README:
# https://github.com/openedx/codejail).
#
# Some of this structure can be changed, and some cannot. Any changes that are
# possible will also need to be coordinated with changes to the apparmor profile
# as well as to the `CODE_JAIL` Django settings. Accordingly, it's best to just
# *avoid* making changes to this part.

# The location of the virtualenv that code executions in the sandbox will use.
# This is a critical path, as SAND_VENV/bin/python is what is targeted by the
# AppArmor confinement. It must also match the Django setting
# `CODE_JAIL.python_bin`. The codejail docs refer to this as `<SANDENV>`.
ARG SAND_VENV=/sandbox/venv
# The user account that will run code executions, described just as "the sandbox
# user" in codejail docs. This needs to match the Django setting
# `CODE_JAIL.user` and the sudoers file.
ARG SAND_USER=sandbox
# Same situation as for APP_UID
ARG SAND_UID=33552349
ARG SAND_GID=$SAND_UID
# The user account that runs the regular web app, described in codejail docs as
# `<SANDBOX_CALLER>`. Needs to match the sudoers file.
ARG APP_USER=app

# The codejail-service API tests check for the visibility of this environment
# variable from the sandbox. (It should not be visible.) This helps test for
# environment leakage into the sandbox.
ENV CJS_TEST_ENV_LEAKAGE=yes

# Packages installed:
#
# - language-pack-en, locales: Ubuntu locale support so that system utilities
#   have a consistent language and time zone.
# - sudo: Web user (`APP_USER`) needs to be able to sudo as `SAND_USER`
# - python*: Specific versions of Python -- the service runs with a recent version, but
#   the sandboxed code will usually need a different (older) version. This is also why
#   we need to pull in the deadsnakes PPA.
# - python*-dev: Header files for python extensions, required by many source wheels
# - python*-venv: Allow creation of virtualenvs
#
# We also have to do a bit of bootstrapping here installing the
# `software-properties-common` package gives us `add-apt-repository`, which
# allows us to add the deadsnakes PPA more easily (that is, without messing
# about with repository keys).
RUN <<EOCMD
  set -eu
  apt-get update
  ${APT_INSTALL} \
    software-properties-common \
  ;
  add-apt-repository ppa:deadsnakes/ppa
  ${APT_INSTALL} \
    language-pack-en \
    locales \
    python${APP_PY_VER} \
    python${APP_PY_VER}-dev \
    python${APP_PY_VER}-venv \
    python${SANDBOX_PY_VER} \
    python${SANDBOX_PY_VER}-venv \
    sudo  \
  ;
EOCMD

RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# We'll build the virtualenv and pre-compile Python as root, but switch to app user
# for actually running the application.
RUN groupadd --gid $APP_GID $APP_USER
RUN useradd --no-log-init --no-create-home --shell /bin/false --uid $APP_UID --gid $APP_GID $APP_USER

COPY --from=codejail-service-code / /app

WORKDIR /app

RUN <<EOCMD
    set -eu
    python${APP_PY_VER} -m venv /venv
    /venv/bin/pip install -r /app/requirements/pip.txt
    /venv/bin/pip install -r /app/requirements/pip-tools.txt
EOCMD

##### Sandbox environment #####

# Codejail executions will be run under this user's account.
RUN groupadd --gid $SAND_GID $SAND_USER
RUN useradd --no-log-init --no-create-home --shell /bin/false --uid $SAND_UID --gid $SAND_GID $SAND_USER

# We need to use --copies so that there is a distinct Python
# executable to confine.
RUN mkdir -p ${SAND_VENV}
RUN python${SANDBOX_PY_VER} -m venv --clear --copies ${SAND_VENV}

# Install the Python libraries used by the sandbox.
RUN --mount=type=bind,from=sandbox-dependencies,source=/,target=/tmp/sandbox-dependencies <<EOCMD
    ${SAND_VENV}/bin/pip install -r /tmp/sandbox-dependencies/${SANDBOX_DEPS_SRC_FILE} \
{%- for extra_requirements in CODEJAIL_EXTRA_PIP_REQUIREMENTS %}
    '{{ extra_requirements }}' \
{%- endfor %}
    ;
EOCMD


# Sudoers config as specified by codejail's docs.
# - `find` is used in sandbox cleanup
# - `pkill` is used to terminate overlong execution
COPY <<01-sandbox /etc/sudoers.d/
${APP_USER} ALL=(${SAND_USER}) SETENV:NOPASSWD:${SAND_VENV}/bin/python
${APP_USER} ALL=(${SAND_USER}) SETENV:NOPASSWD:/usr/bin/find
${APP_USER} ALL=(ALL) NOPASSWD:/usr/bin/pkill
01-sandbox

ENV PATH="/venv/bin:$PATH"

FROM app AS prod

RUN /venv/bin/pip-sync requirements/base.txt
RUN python${APP_PY_VER} -m compileall /venv /app

# Drop to unprivileged user for running service
USER ${APP_USER}

CMD [ "gunicorn", \
    "--config=/app/codejail_service/docker_gunicorn_configuration.py", \
    "--name=codejail-service", \
    "--bind=0.0.0.0:8550",  \
    "--max-requests=1000",  \
    "--log-file=-", \
    "codejail_service.wsgi:application" ]
