from app.Core.Services.BaseService import BaseService
from app.Data.Models.PersonQuiz import PersonQuiz


class PersonQuizService(BaseService):
    def __init__(self) -> None:
        super().__init__(PersonQuiz)