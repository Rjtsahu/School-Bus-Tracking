from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from BusTrack.repository import Base
from BusTrack.repository.models import STRING_LEN_SMALL


class Attendance(Base):
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True)
    is_pick_present = Column(Boolean, default=0)
    is_drop_present = Column(Boolean, default=0)
    pick_gps = Column(String(STRING_LEN_SMALL))
    drop_gps = Column(String(STRING_LEN_SMALL))
    pick_time = Column(DateTime, nullable=True)
    drop_time = Column(DateTime, nullable=True)

    kid_id = Column(ForeignKey('kid.id'))
    journey_id = Column(ForeignKey('journey.id'))
