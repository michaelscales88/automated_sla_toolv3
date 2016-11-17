import sqlite3 as lite
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker


class SqliteWriter:
    def __init__(self, local_db):
        engine = create_engine("sqlite://{0}".format(local_db))
        # self.base = DailyMars()
        self.session = sessionmaker(bind=engine)


# class DailyMars(declarative_base):
#     __tablename__ = 'daily_mars'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     weight = Column(Float)
#     birth = Column(Date)