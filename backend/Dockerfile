FROM python:3.12-slim

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=2.1.1

RUN pip install poetry==${POETRY_VERSION}


WORKDIR /app

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry install --no-root --only main

COPY ./backend ./backend

ENV TEMPLATE_DIR=/app/backend/templates

RUN chmod +x /app/backend/entrypoint.sh /app/backend/generate_keys.sh

ENTRYPOINT ["/app/backend/entrypoint.sh"]
