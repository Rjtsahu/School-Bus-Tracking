from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

ENGINE_CONNECTION_STRING = 'sqlite:///data.db'


# create sqlite database engine.
engine = create_engine(ENGINE_CONNECTION_STRING, echo=True)
session_maker = sessionmaker(bind=engine)
session = session_maker()

Base = declarative_base()
