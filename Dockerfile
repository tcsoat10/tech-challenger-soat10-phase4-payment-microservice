FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl \
    netcat-openbsd \
    build-essential \
    libpq-dev \
    && apt-get clean

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-ansi

COPY . .

RUN rm -rf /app/.venv

RUN chmod +x /app/config/init_db/init_db.sh

ARG PORT=8000
ENV PORT=${PORT}
EXPOSE ${PORT}

CMD ["sh", "-c", "./config/init_db/init_db.sh && poetry run uvicorn src.app:app --host 0.0.0.0 --port $PORT"]
