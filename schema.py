from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tasks(Base):
   __tablename__ = 'tasks'
   id = Column(Integer, primary_key=True)
   title = Column(String)
   description = Column(String)
   done = Column(Boolean)

