from src.base_dao import BaseDAO
from src.history.models import HistoryModel
from src.history.schemas import History


class HistoryDAO(BaseDAO[HistoryModel, History, History]):
    model = HistoryModel
