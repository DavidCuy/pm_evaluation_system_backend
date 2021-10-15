from __future__ import annotations
from typing import Dict, List, Type
from sqlalchemy import Column, Integer, orm
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.query import Query
from typing import List

from sqlalchemy.orm import declarative_base

Base = declarative_base()

class BaseModel(Base):
    """ Base model for a child classes implementations

    Args:
        Base (Any): SQLAlchemy declarative base

    Raises:
        e: Exceptions for not implemented functions

    Returns:
        BaseModel: Instace of BaseModel class
    """

    ## Indicate it is an abstract class (not 100% completed y going to be done in child classes)
    __abstract__ = True
    ## Model identifier. All tables from database should have
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_path_name = ""

    @property
    def attrs(self) -> List[str]:
        """ Returns a list of the attributes of an object

        Returns:
            List[str]: Attributes
        """
        preliminar = list(filter(lambda prop: not str(prop).startswith('_'), type(self).__dict__.keys()))
        display_member = self.display_members()
        return list(set(preliminar) & set(display_member)) if len(display_member) > 0 else display_member

    @classmethod
    def all(cls_, session: Session):
        """ Get all rows from a table

        Args:
            cls_ (cls): Type of class
            session (Session): Database session

        Returns:
            List[Type[BaseModel]]: List of elements mapped from database table
        """
        return session.query(cls_).all()
    
    @classmethod
    def get_paginated(cls_, session: Session, page: int = 1, per_page: int = 10):
        page = page - 1
        query = session.query(cls_).order_by(cls_.id.asc()).limit(per_page).offset(page*per_page)
        return query.all()
    
    @classmethod
    def find(cls_, session: Session, id: int):
        """ Search a row by id

        Args:
            cls_ (class): Child class method
            session (Session): Database session
            id (int): Row identifier

        Returns:
            Type[BaseModel]: The row that have a coincidence with the identifier
        """
        if int(id) > 0:
            return session.query(cls_).get(id)
    
    @classmethod
    def filter_by(cls_, session: Session, column_name: str, value, paginated: bool = False, page: int = 1, per_page: int = 10, first = False):
        """ Gets all rows that match with the specified filter

        Args:
            cls_ (class): Child class method
            session (Session): Database session
            column_name (str): Column name to filter
            value (Any): Value to match

        Returns:
            List[Type[BaseModel]]: List of elements that match with filter
        """
        filter_dict = {
            column_name: value
        }
        query = session.query(cls_).filter_by(**filter_dict).order_by(cls_.id.asc())

        if first:
            return query.first()

        if paginated:
            page = page - 1
            query = query.limit(per_page).offset(page*per_page)
            return query.all()
        return query.all()
    
    @classmethod
    def get_one(cls_, session: Session, column_name: str, value):
        """ Gets the first row that matches the filter

        Args:
            cls_ (class): Child class method
            session (Session): Database session
            column_name (str): Column name to filter
            value (Any): Value to match

        Returns:
            Type[BaseModel]: First register that match with filter
        """
        filter_dict = {
            column_name: value
        }
        return session.query(cls_).filter_by(**filter_dict).first()
    
    @classmethod
    def filters(cls_, session: Session, filters: List[dict], paginated: bool = False, page: int = 1, per_page: int = 10, first: bool = False):
        """ Gets all rows that match with the multiple filters specified in dict (and logic)

        Args:
            cls_ (class): Child class method
            session (Session): Database session

        Returns:
            List[Type[BaseModel]]: List of elements that match with the multiple filters
        """
        query = session.query(cls_)

        for filter in filters:
            query = query.filter_by(**filter)
        
        query = query.order_by(cls_.id.asc())

        if first:
            return query.first()
        
        if paginated:
            page = page - 1
            query = query.limit(per_page).offset(page*per_page)
            return query.all()
        return query.all()

    def before_save(self, *args, **kwargs):
        """ Method to execute before save a row in database (polimorfism)
        """
        pass

    def after_save(self, *args, **kwargs):
        """ Method to execute after save a row in database (polimorfismo)
        """
        pass
    
    def save(self, session: Session, commit=True):
        """ Save a register in database

        Args:
            session (Session): Database session
            commit (bool, optional): Indicate if the changes will make in database. Defaults to True.

        Raises:
            e: In case of error, the register will be erased and raise an Exception
        """
        self.before_save()
        session.add(self)
        if commit:
            try:
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

        self.after_save()
        return self

    def before_update(self, *args, **kwargs):
        """ Method to execute before update a row in database (polimorfism)
        """
        pass

    def after_update(self, *args, **kwargs):
        """ Method to execute after update a row in database (polimorfism)
        """
        pass

    def update(self, session: Session, object: dict, *args, **kwargs):
        """ Update a specified register in database

        Args:
            session (Session): Database session
            object (dict): Dictionary with only the field to update
        """
        self.before_update(*args, **kwargs)
        keys = self.get_keys()
        for key in keys:
            if key in object:
                self.__setattr__(key, object[key])
                pass

        session.commit()
        self.after_update(*args, **kwargs)
        return self

    def delete(self, session: Session, commit=True):
        """ Delete a specified register in database

        Args:
            session (Session): Database session
            commit (bool, optional): Indicate if the changes will make in database. Defaults to True.
        """
        session.delete(self)
        if commit:
            session.commit()

    @classmethod
    def eager(cls_: Type[BaseModel], session: Session, *args) -> Query:
        """ Execute in one load all joins

        Returns:
            Type[BaseModel]: Database query
        """
        cols = [orm.joinedload(arg) for arg in args]
        return session.query(cls_).options(*cols)
    
    @classmethod
    def count(cls_: Type[BaseModel], session: Session) -> int:
        """ Execute in one load all joins

        Returns:
            Type[BaseModel]: Database query
        """
        return session.query(cls_.id).count()
    
    @classmethod
    def count_with_filters(cls_: Type[BaseModel], session: Session, filters: List[dict]) -> int:
        query = session.query(cls_)

        for filter in filters:
            query = query.filter_by(**filter)
        
        return query.count()
    
    @classmethod
    def get_keys(cls_: Type[BaseModel]) -> List[str]:
        """ Get all attributes of class

        Args:
            cls_ (Type[BaseModel]): Child class method

        Returns:
            List[str]:  Attributes
        """
        return list(filter(lambda prop: not str(prop).startswith('_'), cls_.__dict__.keys()))
    
    def property_map(self) -> Dict[str, str]:
        """Remap property with display value

        Returns:
            Dict[str, str]: Dict of string with key as class property name and value as display
        """
        return {}
    
    def display_members(self) -> List[str]:
        """Get only de properties to display to end user

        Returns:
            List[str]: List of properties
        """
        return []


    def __repr__(self) -> str:
        """ Model representation

        Returns:
            str: Model output string formatted
        """
        attr_array = [f"{attr}={self.__getattribute__(attr)}" for attr in self.attrs]
        args_format = ",".join(attr_array)
        return f"<{type(self).__name__}({args_format})>"
