from operator import index
from turtle import title
from sqlalchemy import Column,Integer,String
from .db import Base

class User(Base):

    __tablename__ = 'blog'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
