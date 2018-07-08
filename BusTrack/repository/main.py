from BusTrack.repository import Base
from BusTrack.repository import engine

# import all relevant db models here.
from BusTrack.repository.models.Bus import Bus


def create_database():
    print('creating database from given mappings')
    Base.metadata.create_all(engine)
    Bus.__create_default_bus__()
    print('created mapping')
