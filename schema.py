from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.engine.url import URL

Base = declarative_base()

class Tasks(Base):
   __tablename__ = 'tasks'
   id = Column(Integer, primary_key = True, autoincrement=True, nullable=False)
   title = Column(String, nullable=False)
   description = Column(String)
   done = Column(Boolean, default=False)
   date = Column(DateTime, default=datetime.utcnow)

   def create_db(self, Base):

      engine = create_engine('sqlite:///tasks.db', echo = True)

      # create tables
      Base.metadata.create_all(bind=engine)

      # create session
      Session = sessionmaker()
      Session.configure(bind=engine)
      session = Session()

      try:
         # add row to database
         row = Tasks(title="Read a book", description="Currently reading Neuromancer")
         session.add(row)
         session.commit()

         # update row to database
         row = session.query(Tasks).filter(
               Tasks.title == 'Read a book').first()
         row.title = "Read two books"
         row.description = "Both Science Fiction"
         session.commit()

         # check update correct
         row = session.query(Tasks).filter(
               Tasks.title == 'Read two books').first()
         print('update:', row.title, row.description)
      except SQLAlchemyError as e:
         print(e)
      finally:
         session.close()

# Sample Data
#    [
#    {'title':'Read a book','description':'Currently reading Neuromancer', 'done':False, 'date': datetime.utcnow},
#    {'title':'Play League','description':'Gotte climb those ranks', 'done':False, 'date': datetime.utcnow},
#    {'title':'Study design patterns','description':'Ugh', 'done':False, 'date': datetime.utcnow},
#    {'title':'Buy a cake','description':'Maybe two', 'done':False, 'date': datetime.utcnow},
#    ]
