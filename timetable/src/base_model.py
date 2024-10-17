from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData


# Base DAO class
class Base(DeclarativeBase):
    metadata = MetaData()