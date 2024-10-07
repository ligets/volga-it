from . import BaseDAO
from ..models.RefreshSessionModel import RefreshSessionModel
from ..schemas.AuthSchemas import RefreshSessionCreate, RefreshSessionUpdate


class RefreshSessionDAO(BaseDAO[RefreshSessionModel, RefreshSessionCreate, RefreshSessionUpdate]):
    model = RefreshSessionModel

