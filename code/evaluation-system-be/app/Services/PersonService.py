from app.Core.Services.BaseService import BaseService
from app.Data.Models.Person import Person


class PersonService(BaseService):
    def __init__(self) -> None:
        super().__init__(Person)