from app.Core.Services.BaseService import BaseService
from app.Data.Models.Quiz import Quiz


class QuizService(BaseService):
    def __init__(self) -> None:
        super().__init__(Quiz)