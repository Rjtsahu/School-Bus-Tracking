from sqlalchemy import Boolean, Column, String, Integer
from BusTrack.repository import Base, session


class Bus(Base):
    __tablename__ = 'bus'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    detail = Column(String(200))
    vehicle_number = Column(String(40))
    capacity = Column(Integer, default=40)
    is_active = Column(Boolean, default=True)

    @staticmethod
    def __create_default_bus__():
        if session.query(Bus).count == 0:
            default_bus = Bus()
            default_bus.name = 'test bus'
            default_bus.detail = 'default bus'
            default_bus.vehicle_number = 'MP-22-2525'

            session.add(default_bus)
            session.commit()
            session.close()
