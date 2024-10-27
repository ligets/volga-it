from pydantic import BaseModel


class ErrorResponseModel(BaseModel):
    detail: str
