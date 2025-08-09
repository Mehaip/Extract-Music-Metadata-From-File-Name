from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:///db/data.db')
Session = sessionmaker(bind=engine)

def create_all_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(engine)