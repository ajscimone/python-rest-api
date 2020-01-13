from sqlalchemy import create_engine, Table, Column, Integer, String, Boolean, DateTime, MetaData
from datetime import datetime

meta = MetaData()

db = create_engine('sqlite:///tasks.db', echo = True)

meta = MetaData(db)

tasks_table = Table(
   'tasks', meta, 
   Column('id', Integer, primary_key = True, autoincrement=True), 
   Column('title', String), 
   Column('description', String), 
   Column('done', Boolean), 
   Column('date', DateTime)
)

meta.create_all()

conn = db.connect()

conn.execute(tasks_table.insert(),[
   {'title':'Read a book','description':'Currently reading Neuromancer', 'done':False, 'date': datetime.utcnow},
   {'title':'Play League','description':'Gotte climb those ranks', 'done':False, 'date': datetime.utcnow},
   {'title':'Study design patterns','description':'Ugh', 'done':False, 'date': datetime.utcnow},
   {'title':'Buy a cake','description':'Maybe two', 'done':False, 'date': datetime.utcnow},
   ])