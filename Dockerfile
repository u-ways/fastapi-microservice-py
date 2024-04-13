# An optimised multistaged Dockerfile for Poetry.
# Based of https://github.com/python-poetry/poetry/discussions/1879?sort=top#discussioncomment-216865

################################
# PYTHON-BASE
# Sets up all our shared environment variables
################################
FROM python:3.11-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # see: https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.8.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    # paths this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    # where the virtual environment will be created
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

################################
# BUILDER-BASE
# Used to build deps + create our virtual environment
################################
FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl \
        # deps for building python deps
        build-essential

# Installs poetry - respects $POETRY_VERSION & $POETRY_HOME
# The --mount will mount the buildx cache directory to where
# Poetry and Pip store their cache so that they can re-use it
RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python3 -

# Switch to the directory with our poetry files
WORKDIR $PYSETUP_PATH

# Copy project requirement files here to ensure they will be cached.
COPY poetry.lock pyproject.toml ./

# Install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN --mount=type=cache,target=/root/.cache \
    poetry install --without=dev --no-root


################################
# DEVELOPMENT
# Image used during development / testing
################################
FROM python-base as development

ENV FASTAPI_ENV=development
ENV PYTHONPATH="/app/src:$PYTHONPATH"

# Switch to the directory with our poetry files
WORKDIR $PYSETUP_PATH

# Copy in our built poetry + venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# Quicker install as runtime deps are already installed
RUN --mount=type=cache,target=/root/.cache \
    poetry install --with=dev

WORKDIR /app

# NOTE:
# In the development image we don't copy in our codebase
# We expect the user to mount their code into the container

EXPOSE 8000:8000
CMD ["uvicorn", "src.main:app", "--app-dir", "./src", "--host", "0.0.0.0", "--port", "8000", "--reload"]


################################
# PRODUCTION
# Final image used for runtime
################################
FROM python-base as production

ARG APP_NAME
ARG APP_VERSION

ENV FASTAPI_ENV=production
ENV PYTHONPATH="/app/src:$PYTHONPATH"
ENV APP_VERSION=${APP_VERSION}

COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY ./src /app/src
COPY .env ./

WORKDIR /app

LABEL app="${APP_NAME}" \
      maintainer="U-ways (work@u-ways.info)" \
      description="A maintainable FastAPI microservice proof of concept." \
      url="https://github.com/u-ways/fastapi-microservice-py"

# see: https://fastapi.tiangolo.com/deployment/docker/#deploy-the-container-image
CMD ["uvicorn", "src.main:app", "--app-dir", "./src", "--host", "0.0.0.0", "--port", "80"]