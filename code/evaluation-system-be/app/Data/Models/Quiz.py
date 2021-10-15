from typing import Dict, List
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from ...Core.Data.BaseModel import BaseModel

class Quiz(BaseModel):
    """ Table Quizzes Database model

    Args:
        BaseModel (ORMClass): Parent class

    Returns:
        Quiz: Instance of model
    """

    __tablename__ = 'Quizzes'
    id = Column("IdQuiz", Integer, primary_key=True)
    Name = Column("Name", String, nullable=False)
    Description = Column("Description", String, nullable=True)
    
    model_path_name = "quizzes"
    
    def property_map(self) -> Dict:
        return {
            "id": "IdQuiz"
        }
    
    def display_members(self) -> List[str]:
        return [
            "id", "Name", "CountryCode", "Description"
        ]
