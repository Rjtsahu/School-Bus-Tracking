from sqlalchemy import Boolean, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from BusTrack.repository import Base
from BusTrack.repository.models import STRING_LEN_SMALL, STRING_LEN_MEDIUM, STRING_LEN_LARGE, LEN_MOBILE

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(STRING_LEN_MEDIUM))
    last_name = Column(String(STRING_LEN_MEDIUM))
    phone = Column(String(LEN_MOBILE))
    address = Column(String(STRING_LEN_LARGE))
    city = Column(String(STRING_LEN_SMALL))
    state = Column(String(STRING_LEN_SMALL))
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey('user_type.id'))
    user_role = relationship("UserType", backref=backref("user", uselist=False))

    full_name = first_name + ' ' + last_name
    kids = relationship("Kid", backref=backref("user", uselist=True))

