"""
user_models.tables

This module defines the SQLAlchemy models for the user management system.
It includes the UserInfo model, which represents the user information stored in the database.

Dependencies:
- SQLAlchemy: Provides ORM capabilities and database interaction.
- db_connections.configurations: Imports Base for model definition.

Models:
- UserInfo: Represents a user in the database with attributes for EmployeeID, Age, Name, Exp, Gender, Dept, and Country.
"""
# user_models/tables.py
from sqlalchemy import Column, String, Integer, Float
from db_connections.configurations import Base


# Define the UserInfo model
class UserInfo(Base):
    """
       Defines the UserInfo model for the user_info table.

       This model represents the user information stored in the database with the following attributes:
       - EmployeeID: The unique identifier for the employee (Primary Key).
       - Age: The age of the employee.
       - Name: The name of the employee.
       - Exp: The years of experience of the employee.
       - Gender: The gender of the employee.
       - Dept: The department in which the employee works.
       - Country: The country where the employee is located.
       """
    __tablename__ = "user_info"
    EmployeeID = Column("emp_id", Integer, primary_key=True)
    Age = Column("age", Integer)
    Name = Column("name", String)
    Exp = Column("exp", Float)
    Gender = Column("gender", String)
    Dept = Column("dept", String)
    Country = Column("country", String)
