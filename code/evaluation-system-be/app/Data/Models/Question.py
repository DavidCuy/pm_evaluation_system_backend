from typing import Dict, List
from sqlalchemy import Column, Integer, String, DateTime
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
    IdQuiz = Column("IdQuiz", Integer, nullable=False)
    Description = Column("Description", String, nullable=True)

    quiz = relationship("Quiz", back_populates="questions")
    answers = relationship("Answer", back_populates="question")
    
    model_path_name = "questions"
    
    def property_map(self) -> Dict:
        return {
            "id": "IdQuestion"
        }
    
    def display_members(self) -> List[str]:
        return [
            "id", "Description"
        ]
