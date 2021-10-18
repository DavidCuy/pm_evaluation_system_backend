from typing import Dict, List
from sqlalchemy import Column, Integer
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
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
    
        
