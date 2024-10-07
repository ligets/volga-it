<h1 align="center">Volga-it - Backend разработка</h1>
<pre align="center">Репозиторий размещен как решение задания полуфинального этапа дисциплины «Backend разработка: Web API»</pre>

## Основное задание:
1. Account URL: [http://localhost:8081/ui-swagger](http://localhost:8081/ui-swagger)
2. Hospital URL: [http://localhost:8082/ui-swagger](http://localhost:8082/ui-swagger)
3. Timetable URL: [http://localhost:8083/ui-swagger](http://localhost:8083/ui-swagger)
4. Document URL: [http://localhost:8084/ui-swagger](http://localhost:8084/ui-swagger)

## Дополнительное задание:
1. ElastickSearch URL: http://elasticksearch-service
2. Kibana URL: http://kibana-service/

## Дополнительная информация
1. Запуск решения:
    * Скопировать репозиторий с помощью команды ```git clone https://github.com/ligets/volga.git``` или скачать в zip архиве и распокавать
    * Если вы используете docker-compose версии где требуется указывать тэг version, то раскомментируйте 1-ую строку в файле docker-compose.yaml
    * Запустить решение с помощью команды <code>docker-compose up --build -d</code>

2. Все id: int заменены на id: UUID, кроме (БД - Таблица - Поле):
    * account_db - roles - id

3. Используемый стек разработки: 
    * Postgres - Основная СУБД
    * Python - Язык программирования на котором разработано решение 
    * FastAPI - Фреймворк на котором разрабатывалось решение
    * Pydantic - Библиотека для валидации и сериализации данных
    * Alembic - Миграции баз данных микросервисов
    * SQLAlchemy - ORM система для запросов в БД
    * AsyncPg - Асинхронная библиотека для работы с PostgreSQL
    * Python-jose - Библиотека для подписи и верификации JWT-токенов (используется в микросервисе аккаунтов)
    * PyJWT - Библиотека использовалась для извлечения данных из JWT-токенов (использовалась во всех микросервисах кроме микросервиса аккаунтов)
    * Httpx - Библиотека для связи микросервисов по http протоколу
