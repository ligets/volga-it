import os
import sys
import time
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from elasticsearch import ElasticsearchWarning

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import all_routers
from src.database import es
from src.config import logger


@asynccontextmanager
async def lifespan(_: FastAPI):
    while True:
        try:
            if await es.ping():
                logger.info("Успешное подключение к ElasticSearch")
                break
            logger.error("Не удалось подключиться к ElasticSearch. Переподключение через 5 секунд...")
        except ElasticsearchWarning as e:
            logger.error(f"Ошибка ElasticSearch: {e}")
        time.sleep(5)

    try:
        if not await es.indices.exists(index='history'):
            await es.indices.create(index='history', body={
                "mappings": {
                    "properties": {
                        "id": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "date": {
                            "type": "date"
                        },
                        "pacientId": {
                            "type": "keyword"
                        },
                        "hospitalId": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "doctorId": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "room": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "data": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        }
                    }
                }
            })
        yield
    finally:
        await es.close()

app = FastAPI(
    title="Document microservice",
    docs_url="/ui-swagger",
    lifespan=lifespan
)

app.include_router(
    all_routers,
    prefix="/api"
)


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8084, log_level='error')
