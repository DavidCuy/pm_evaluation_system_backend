from typing import Dict, List
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from ...Core.Data.BaseModel import BaseModel

class Question(BaseModel):
    """ Table Questions Database model

    Args:
        BaseModel (ORMClass): Parent class

    Returns:
        Question: Instance of model
    """

    __tablename__ = 'Questions'
    id = Column("IdQuestion", Integer, primary_key=True)
    IdQuiz = Column("IdQuiz", Integer, ForeignKey('Quizzes.IdQuiz'))
    Description = Column("Description", String, nullable=True)

    quiz = relationship("Quiz", back_populates="questions")
    
    model_path_name = "questions"
    
    def property_map(self) -> Dict:
        return {
            "id": "IdQuestion"
        }
    
    def display_members(self) -> List[str]:
        return [
            "id", "Description"
        ]
