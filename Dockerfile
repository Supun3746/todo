FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /todo

COPY pyproject.toml poetry.lock* /todo/

RUN poetry config virtualenvs.create false && poetry install --no-root

COPY . .

VOLUME ["/sqlite3.db"]

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]