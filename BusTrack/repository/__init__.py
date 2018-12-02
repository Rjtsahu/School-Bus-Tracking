from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import StaticPool

ENGINE_CONNECTION_STRING = 'sqlite:///data.db'

# create sqlite database engine.
# these setting's are applicable for sqlite3 only.
engine = create_engine(ENGINE_CONNECTION_STRING, echo=True, connect_args={'check_same_thread': False},
                       poolclass=StaticPool)
session_maker = sessionmaker(bind=engine)
session = session_maker()

Base = declarative_base()
