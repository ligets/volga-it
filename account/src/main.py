import asyncio
import os.path
import sys
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import settings
from src.rabbitMq.server import consume_rabbitmq
from src import all_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}",
        encoding='utf-8',
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix='account')
    task = asyncio.create_task(consume_rabbitmq())
    try:
        yield
    finally:
        task.cancel()
        await redis.close()


app = FastAPI(
    title="Account microservice",
    docs_url='/ui-swagger',
    lifespan=lifespan
)

app.include_router(
    all_router,
    prefix='/api'
)


app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods='*',
    allow_headers='*',
)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8081, log_level='error')
