from app.Core.Services.BaseService import BaseService
from app.Data.Models.Question import Question


class QuestionService(BaseService):
    def __init__(self) -> None:
        super().__init__(Question)