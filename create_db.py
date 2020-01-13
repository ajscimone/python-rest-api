from sqlalchemy import create_engine, Table, Column, Integer, String, Boolean, MetaData
meta = MetaData()

db = create_engine('sqlite:///tasks.db', echo = True)

meta = MetaData()

tasks = Table(
   'tasks', meta, 
   Column('id', Integer, primary_key = True), 
   Column('title', String), 
   Column('description', String), 
   Column('done', Boolean), 
)

meta.create_all(db)