from typing import Dict, List
from sqlalchemy import Column, Integer
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from app.Data.Enum.http_status_code import HTTPStatusCode
from app.Data.Models.Answer import Answer

from app.Data.Models.Question import Question
from app.Exceptions.APIException import APIException
from ...Core.Data.BaseModel import BaseModel
from .Quiz import Quiz
from .Person import Person

class PersonAnswer(BaseModel):
    """ Table PersonsAnwers Database model

    Args:
        BaseModel (ORMClass): Parent class

    Returns:
        Quiz: Instance of model
    """

    __tablename__ = 'PersonsAnwers'
    id = Column("IdPersonAnswer", Integer, primary_key=True)
    IdPerson = Column("IdPerson", Integer, ForeignKey(Person.id))
    IdAnswer = Column("IdAnswer", Integer, ForeignKey(Quiz.id))
    
    model_path_name = "persons-answers"

    person = relationship(Person)
    quiz = relationship(Quiz)
    
    def property_map(self) -> Dict:
        return {
            "id": "PersonAnwer"
        }
    
    def display_members(self) -> List[str]:
        return [
            "id", "IdPerson", "IdAnswer"
        ]
    
    def before_save(self, sesion: Session, *args, **kwargs):
        answer = sesion.query(Answer).get(self.IdAnswer)

        filter_dict = {"IdQuestion": answer.IdQuestion}
        answer_ids = list(map(lambda a: a.id, sesion.query(Answer).filter_by(**filter_dict).all()))
        answered = sesion.query(PersonAnswer).filter(PersonAnswer.IdAnswer.in_(answer_ids)).count()
        print(answer_ids)
        print(answered)

        if (self.IdAnswer in answer_ids) and (answered > 0):
            raise APIException("Cannot add more than 1 answer per question", status_code = HTTPStatusCode.NOT_ACCEPTABLE.value)
        
