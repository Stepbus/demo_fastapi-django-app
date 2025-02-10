FROM python:3.12-slim

ARG POETRY_VERSION=2.0.0

RUN apt-get update && apt-get install -y \
    libpq-dev gcc curl pkg-config && \
    apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip==24.* cryptography==43.* --no-cache-dir

RUN curl -sSL https://install.python-poetry.org | python3 - --version ${POETRY_VERSION}

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock README.md /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root \
    && rm -rf ~/.cache/pypoetry

COPY src/ /app/src/
COPY scripts/ /app/scripts

RUN chmod +x /app/scripts/entrypoint.sh
