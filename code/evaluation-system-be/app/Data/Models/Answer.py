import logging
from typing import Dict, List
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ...Data.Enum.http_status_code import HTTPStatusCode
from ...Exceptions.APIException import APIException
from ...Core.Data.BaseModel import BaseModel
from .Question import Question

class Answer(BaseModel):
    """ Table Answers Database model

    Args:
        BaseModel (ORMClass): Parent class

    Returns:
        Answer: Instance of model
    """

    __tablename__ = 'Answers'
    id = Column("IdAnswer", Integer, primary_key=True)
    IdQuestion = Column("IdQuestion", Integer, ForeignKey(Question.id))
    Description = Column("Description", String, nullable=True)
    Correct = Column("Correct", Boolean, nullable=True)

    question = relationship(Question)
    
    model_path_name = "answers"
    
    def property_map(self) -> Dict:
        return {
            "id": "IdAnswer"
        }
    
    def display_members(self) -> List[str]:
        return [
            "id", "Description", "Correct"
        ]

    def before_save(self, sesion: Session, *args, **kwargs):
        max_answers_filter = {
            "IdQuestion": self.IdQuestion
        }

        base_query = sesion.query(Answer).filter_by(**max_answers_filter)

        if base_query.count() >= 4:
            raise APIException("Cannot add more than 4 answers per question", status_code = HTTPStatusCode.NOT_ACCEPTABLE.value)
        
        at_least_one_correct_filter = {
            "Correct": True
        }
        
        if base_query.filter_by(**at_least_one_correct_filter).count() > 0 and self.Correct == True:
            raise APIException("No more of 2 correct answer per question", status_code = HTTPStatusCode.NOT_ACCEPTABLE.value)
        
        if base_query.count() == 3 and base_query.filter_by(**at_least_one_correct_filter).count() < 1 and self.Correct == False:
            raise APIException("At least one answer should be correct", status_code=HTTPStatusCode.NOT_ACCEPTABLE.value)
    
    def before_update(self, sesion: Session, *args, **kwargs):
        max_answers_filter = {
            "IdQuestion": self.IdQuestion,
        }

        base_query = sesion.query(Answer).filter_by(**max_answers_filter)
        answer_count = base_query.count()
        
        at_least_one_correct_filter = {
            "Correct": True
        }
        if "Correct" in kwargs:
            correct_answers_count = base_query.filter_by(**at_least_one_correct_filter).count()

            if correct_answers_count > 0 and kwargs["Correct"] is True and self.Correct is False:
                raise APIException("No more of 2 correct answer per question", status_code = HTTPStatusCode.NOT_ACCEPTABLE.value)
            if correct_answers_count > 0 and kwargs["Correct"] is False and self.Correct is True:
                raise APIException("At least one answer should be correct", status_code=HTTPStatusCode.NOT_ACCEPTABLE.value)
            if answer_count == 4 and kwargs["Correct"] is False and self.Correct is True:
                raise APIException("At least one answer should be correct", status_code=HTTPStatusCode.NOT_ACCEPTABLE.value)