# -*- coding:utf-8 -*-
"""
author = Barnett
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .config import *

username = USERNAME
password = PASSWORD
host = HOST
port = PORT
db = DATEBASE

__all__ = ['Base', 'engine', 'load_session', 'create_table']

Base = declarative_base()

engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8')


def load_session():
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    session = Session()
    return session


def create_table():
    Base.metadata.create_all(engine)
