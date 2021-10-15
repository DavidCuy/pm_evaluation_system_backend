from typing import Dict, List
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ...Core.Data.BaseModel import BaseModel

class Answer(BaseModel):
    """ Table Answers Database model

    Args:
        BaseModel (ORMClass): Parent class

    Returns:
        Answer: Instance of model
    """

    __tablename__ = 'Answers'
    id = Column("IdAnswer", Integer, primary_key=True)
    IdQuestion = Column("IdQuestion", Integer, nullable=False)
    Description = Column("Description", String, nullable=True)

    question = relationship("Question", back_populates="answers")
    
    model_path_name = "answers"
    
    def property_map(self) -> Dict:
        return {
            "id": "IdAnswer"
        }
    
    def display_members(self) -> List[str]:
        return [
            "id", "Description"
        ]
