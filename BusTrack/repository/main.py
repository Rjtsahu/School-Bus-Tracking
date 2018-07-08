from BusTrack.repository import Base
from BusTrack.repository import engine

# import all relevant db models here.
from BusTrack.repository.models.Bus import Bus
from BusTrack.repository.models.UserType import UserType
from BusTrack.repository.models.User import User
from BusTrack.repository.models.UserLogin import UserLogin
from BusTrack.repository.models.Feedback import Feedback
from BusTrack.repository.models.Kid import Kid
from BusTrack.repository.models.Journey import Journey
from BusTrack.repository.models.Location import Location


def create_database():
    print('creating database from given mappings')
    Base.metadata.create_all(engine)
    Bus.__create_default_bus__()
    UserType.__create_default_role__()
    print('created mapping')
