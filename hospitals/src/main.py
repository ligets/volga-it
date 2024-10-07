import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
import uvicorn
from src.routers import all_routers

app = FastAPI(
    title="Hospitals microservice",
    docs_url='/ui-swagger'
)


app.include_router(
    all_routers,
    prefix='/api'
)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8082, log_level='error')
