from sqlalchemy import Boolean, Column, String, Integer
from BusTrack.repository import Base, session
from BusTrack.repository.models import STRING_LEN_SMALL, STRING_LEN_MEDIUM, STRING_LEN_LARGE


class Bus(Base):
    __tablename__ = 'bus'

    id = Column(Integer, primary_key=True)
    name = Column(String(STRING_LEN_MEDIUM))
    detail = Column(String(STRING_LEN_LARGE))
    vehicle_number = Column(String(STRING_LEN_SMALL))
    capacity = Column(Integer, default=40)
    is_active = Column(Boolean, default=True)

    @staticmethod
    def __create_default_bus__():
        if session.query(Bus).count() == 0:
            default_bus = Bus()
            default_bus.name = 'test bus'
            default_bus.detail = 'default bus'
            default_bus.vehicle_number = 'MP-22-2525'

            session.add(default_bus)
            session.commit()
            session.close()
