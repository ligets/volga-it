from pydantic import BaseModel


class RoleSchema(BaseModel):
    id: int
    name: str



