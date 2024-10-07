import os.path
import sys
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.routers import all_router

app = FastAPI(
    title="Account microservice",
    docs_url='/ui-swagger'
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
