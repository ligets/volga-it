FROM python:3.12-slim

RUN mkdir timetable_service
WORKDIR /timetable_service

COPY /pyproject.toml /timetable_service

RUN pip3 install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY . .

CMD ["sh", "-c", "poetry run alembic upgrade head && poetry run python src/main.py"]



