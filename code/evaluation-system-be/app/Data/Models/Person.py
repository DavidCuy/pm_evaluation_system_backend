from typing import Dict, List
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.Core.Data.BaseModel import BaseModel

class Person(BaseModel):
    """ Table Persons Database model

    Args:
        BaseModel (ORMClass): Parent class

    Returns:
        Person: Instance of model
    """

    __tablename__ = 'Persons'
    id = Column("IdPerson", Integer, primary_key=True)
    Name = Column("Name", String, nullable=False)
    
    model_path_name = "persons"
    
    def property_map(self) -> Dict:
        return {
            "id": "IdPerson"
        }
    
    def display_members(self) -> List[str]:
        return [
            "id", "Name"
        ]
