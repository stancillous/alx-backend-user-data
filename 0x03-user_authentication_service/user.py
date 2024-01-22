#!/usr/bin/env python3
from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import declarative_base
""""
creating a model named User for a database table
named users"""

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
