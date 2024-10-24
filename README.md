<h1 align="center"><b>Volga-it - Backend разработка</b></h1>
<pre align="center">Репозиторий размещен как решение задания полуфинального этапа дисциплины «Backend разработка: Web API»</pre>

## __Основное задание:__
1. Account URL: [http://localhost:8081/ui-swagger](http://localhost:8081/ui-swagger)
2. Hospital URL: [http://localhost:8082/ui-swagger](http://localhost:8082/ui-swagger)
3. Timetable URL: [http://localhost:8083/ui-swagger](http://localhost:8083/ui-swagger)
4. Document URL: [http://localhost:8084/ui-swagger](http://localhost:8084/ui-swagger)

## __Дополнительное задание:__
1. ElastickSearch URL: [http://localhost:9200/](http://localhost:9200/)
2. Kibana URL: [http://localhost:5601/](http://localhost:5601/)

## __Дополнительная информация__
1. __Запуск решения:__
    * Скопировать репозиторий с помощью команды ```git clone https://github.com/ligets/volga.git``` или скачать в zip архиве и распокавать
    * Если вы используете docker-compose версии где требуется указывать тэг version, то раскомментируйте 1-ую строку в файле docker-compose.yaml
    * Запустить решение с помощью команды <code>docker-compose up -d</code>

    ---

3. __Изменения зависимостей микросервисов:__
    * При удалении аккаунта доктора или удаление роли 'Doctor' из списка его ролей или удаление больницы удаляются все их расписания и записи

    ---

2. __Все id: int заменены на id: UUID, кроме (БД - Таблица - Поле):__
    * account_db - roles - id
    
    ---

3. __Выевленные нюансы системы:__
    * При выходе из аккаунта AccessToken остается живым до истечения срока жизни, RefreshToken уже будет недействителен.

    ---

3. __Используемый стек разработки:__
    * PostgreSQL - Основная СУБД
    * RabbitMQ - Брокер сообщений
    * ElasticSearch - Поиск документов
    * Kibana - Веб-интерфейс для ElasticSearch
    * Python - Язык программирования на котором разработано решение 
    * FastAPI - Фреймворк на котором разрабатывалось решение
    * Pydantic - Библиотека для валидации и сериализации данных
    * Alembic - Миграции баз данных микросервисов
    * SQLAlchemy - ORM система для запросов в БД
    * AsyncPg - Асинхронная библиотека для работы с PostgreSQL
    * PyJWT - Библиотека для подписи и верификации JWT-токенов
    * Aio_pika - Библиотека для асинхронной связи с rabbitmq
    * Fastapi-cache - Библиотека для кэширования(В задание отключено потому что увидел что в прошлом году за это дисквалифицировали. Весь код связанный с кэшированием закоментирован - писал для себя)
    * Pytest - Библиотека для тестирования функционала(Писал для себя)
    
