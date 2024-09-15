FROM python:3.12.0-slim AS builder

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN python -m pip install --no-cache-dir poetry==1.8.2 \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-interaction


FROM python:3.12.2-slim

COPY --from=builder /app /app/

COPY . ./

ENV VENV_PATH="/app/.venv"

CMD ["/app/.venv/bin/python", "main.py"]