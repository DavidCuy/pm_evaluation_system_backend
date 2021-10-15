from typing import Dict, List
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from ...Core.Data.BaseModel import BaseModel
from .Answer import Answer

class Answer(BaseModel):
    """ Table Answers Database model

    Args:
        BaseModel (ORMClass): Parent class

    Returns:
        Answer: Instance of model
    """

    __tablename__ = 'Answers'
    id = Column("IdAnswer", Integer, primary_key=True)
    IdQuestion = Column("IdQuestion", Integer, ForeignKey(Answer.id))
    Description = Column("Description", String, nullable=True)

    question = relationship(Answer)
    
    model_path_name = "answers"
    
    def property_map(self) -> Dict:
        return {
            "id": "IdAnswer"
        }
    
    def display_members(self) -> List[str]:
        return [
            "id", "Description"
        ]
