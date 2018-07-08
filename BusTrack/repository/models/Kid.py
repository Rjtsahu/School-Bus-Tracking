from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from BusTrack.repository import Base
from BusTrack.repository.models import STRING_LEN_SMALL, STRING_LEN_MEDIUM, STRING_LEN_LARGE


class Kid(Base):
    __tablename__ = 'kid'

    id = Column(Integer, primary_key=True)
    name = Column(String(STRING_LEN_MEDIUM))
    section = Column(String(STRING_LEN_SMALL))
    date_joined = Column(DateTime())
    photo = Column(String(STRING_LEN_LARGE))
    parent_id = Column(ForeignKey('user.id'), nullable=False)
    bus_id = Column(ForeignKey('bus.id'))

    parent = relationship("User", backref=backref("kid", uselist=False))
    bus = relationship("Bus", backref=backref("kid", uselist=False))
