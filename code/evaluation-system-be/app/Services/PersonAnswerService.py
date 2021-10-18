from app.Core.Services.BaseService import BaseService
from app.Data.Models.PersonAnswer import PersonAnswer


class PersonAnswerService(BaseService):
    def __init__(self) -> None:
        super().__init__(PersonAnswer)