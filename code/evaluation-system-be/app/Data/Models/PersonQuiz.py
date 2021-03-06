from typing import Dict, List
from sqlalchemy import Column, Integer
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from ...Core.Data.BaseModel import BaseModel
from .Quiz import Quiz
from .Person import Person

class PersonQuiz(BaseModel):
    """ Table PersonsQuizzes Database model

    Args:
        BaseModel (ORMClass): Parent class

    Returns:
        Quiz: Instance of model
    """

    __tablename__ = 'PersonsQuizzes'
    id = Column("IdPersonQuiz", Integer, primary_key=True)
    IdPerson = Column("IdPerson", Integer, ForeignKey(Person.id))
    IdQuiz = Column("IdQuiz", Integer, ForeignKey(Quiz.id))
    
    model_path_name = "persons-quizzes"

    person = relationship(Person)
    quiz = relationship(Quiz)
    
    def property_map(self) -> Dict:
        return {
            "id": "IdPersonQuiz"
        }
    
    def display_members(self) -> List[str]:
        return [
            "id", "IdPerson", "IdQuiz"
        ]
    
        
