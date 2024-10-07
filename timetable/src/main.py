import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI, Depends
import uvicorn

from src.routers import all_routers
from src.dependencies import validate_user_role

app = FastAPI(
    title="Timetable microservice",
    docs_url='/ui-swagger'
)

app.include_router(
    all_routers,
    prefix='/api'
)


@app.get('/test')
async def test(user: dict = Depends(validate_user_role(['Admin', 'Manager']))):
    return {"message": "Hello, you are an admin or manager!"}


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8083, reload=True)
