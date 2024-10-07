FROM python:3.12-slim

RUN mkdir acc_microservice
WORKDIR /acc_microservice

COPY /pyproject.toml /acc_microservice

RUN pip3 install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY . .

CMD ["sh", "-c", "poetry run alembic upgrade head && poetry run python src/main.py"]



