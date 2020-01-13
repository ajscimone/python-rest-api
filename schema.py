from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Task(Base):
   __tablename__ = 'tasks'
   id = Column(Integer, primary_key=True, autoincrement=True)
   title = Column(String)
   description = Column(String)
   done = Column(Boolean)
   date = Column(DateTime, default=datetime.utcnow)
