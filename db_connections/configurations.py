"""
db_connections.configurations

This module provides the database configuration and setup for the SQLAlchemy ORM.
It includes the creation of the SQLAlchemy engine, the Base class for ORM models, and the function
to create all tables in the database.

Dependencies:
- SQLAlchemy: Provides the database connection and ORM functionality.
- sqlalchemy.pool.NullPool: Disables connection pooling.

Configuration:
- DATABASE_URL: The URL for connecting to the PostgreSQL database.
- engine: The SQLAlchemy engine for database interactions.
- Base: The declarative base class for SQLAlchemy ORM models.
- metadata: The SQLAlchemy MetaData instance for database schema.

Functions:
- create_tables: Creates all tables in the database based on the defined ORM models.
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

# SQLAlchemy Base and Metadata
Base = declarative_base()
"""
Base class for all SQLAlchemy ORM models. It provides the foundational class
that maintains a catalog of classes and tables relative to that base.
"""

metadata = MetaData()
"""
MetaData instance used to hold and manage the schema of the database.
"""

# Database configuration
DATABASE_URL = "postgresql://postgres:1995@localhost:5432/postgres"
"""
The URL for connecting to the PostgreSQL database. It includes the database type,
username, password, host, and port.
"""

# Create an engine with NullPool to disable connection pooling
engine = create_engine(DATABASE_URL, echo=True, poolclass=NullPool)
"""
The SQLAlchemy engine used for database interactions. It is configured to connect
to the PostgreSQL database using the DATABASE_URL. NullPool is used to disable
connection pooling, which ensures a new connection is established for each request.
"""

# Create all tables
def create_tables():
    """
    Creates all tables in the database based on the defined ORM models.

    This function uses the Base metadata to create the tables in the database as per
    the ORM models defined in the application. It should be called to initialize
    the database schema before performing any operations.
    """
    Base.metadata.create_all(engine)
