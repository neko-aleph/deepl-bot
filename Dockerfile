FROM python:3.13.4-alpine

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock /app/
COPY src /app/src

RUN poetry config virtualenvs.create false \
 && poetry install --only main

ENTRYPOINT ["poetry", "run", "python", "-m", "deepl_bot.run"]