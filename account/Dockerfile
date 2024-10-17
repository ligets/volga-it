FROM python:3.12-slim

RUN mkdir account_service
WORKDIR /account_service

COPY /pyproject.toml /account_service

RUN pip3 install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi 
    
RUN mkdir -p certificates \
    && openssl genpkey -algorithm RSA -out certificates/private_key.pem -pkeyopt rsa_keygen_bits:2048  \
    && openssl rsa -pubout -in certificates/private_key.pem -out certificates/public_key.pem

COPY . .

CMD ["sh", "-c", "poetry run alembic upgrade head && poetry run python src/main.py"]



