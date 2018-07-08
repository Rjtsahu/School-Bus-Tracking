from sqlalchemy import Boolean, Column, String, Integer, ForeignKey
from BusTrack.repository import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(10))
    address = Column(String(200))
    city = Column(String(100))
    state = Column(String(100))
    is_active = Column(Boolean, default=True)
    person_id = Column(Integer, ForeignKey('user_type.id'))

    full_name = first_name + ' ' + last_name
