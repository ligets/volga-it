from src.base_dao import BaseDAO
from src.authentication.models import RefreshSessionModel
from src.authentication.schemas import RefreshSessionCreate, RefreshSessionUpdate


class RefreshSessionDAO(BaseDAO[RefreshSessionModel, RefreshSessionCreate, RefreshSessionUpdate]):
    model = RefreshSessionModel

