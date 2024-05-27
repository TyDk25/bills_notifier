from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.orm import sessionmaker, declarative_base

"""
Creates SQLite table using sqlalchemy. 
"""

engine = create_engine('sqlite:///bills_notifier.db')

Base = declarative_base()


class Bills(Base):
    __tablename__ = 'Bills'

    id = Column(Integer, primary_key=True)
    Bill_Name = Column(String(50))
    Bill_Amount = Column(Float, nullable=False)
    Bill_Date = Column(Date, nullable=False)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
