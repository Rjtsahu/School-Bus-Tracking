from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from BusTrack.repository import Base
from BusTrack.repository.models import STRING_LEN_SMALL


class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    gps = Column(String(STRING_LEN_SMALL))
    timestamp = Column(DateTime)
    journey_id = Column(ForeignKey('journey.id'))