from enum import Enum

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship, backref

from BusTrack.repository import Base
from BusTrack.repository.models import STRING_LEN_SMALL


class JourneyType(Enum):
    TypeHomeToSchool = 1
    TypeSchoolToHome = 2


class Journey(Base):
    __tablename__ = 'journey'

    id = Column(Integer, primary_key=True)
    type = Column(Integer, default=1)
    date = Column(DateTime())
    start_timestamp = Column(DateTime(), nullable=True)
    end_timestamp = Column(DateTime(), nullable=True)
    latest_gps = Column(String(STRING_LEN_SMALL))
    last_update_timestamp = Column(DateTime(), nullable=True)
    bus_id = Column(ForeignKey('bus.id'))
    bus = relationship('Bus', backref=backref("journey", uselist=False))
    locations = relationship('Location', backref=backref("journey", uselist=True))
