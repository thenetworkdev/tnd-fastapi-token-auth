FROM python:3.9.6-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONASYNCIODEBUG=1 \
    PYTHONTRACEMALLOC=1

# This is only requires if using poetry, if using pip. you can remove the config from line 9 to 19
RUN apt-get update \
    && apt-get install --no-install-recommends -y curl build-essential \
    && apt-get clean

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml poetry.lock ./
RUN poetry install --no-root

# Uncomment the 2 lines below if using pip
# COPY ./requirements.txt ./requirements-dev.txt ./
# RUN pip install -r requirements-dev.txt

WORKDIR /usr/src

CMD uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000