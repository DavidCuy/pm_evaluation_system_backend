from app.Core.Services.BaseService import BaseService
from app.Data.Models.Answer import Answer


class AnswerService(BaseService):
    def __init__(self) -> None:
        super().__init__(Answer)