from sqlalchemy import Boolean, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from BusTrack.repository import Base
from BusTrack.repository.models import STRING_LEN_SMALL, STRING_LEN_LARGE, LEN_MOBILE


class UserLogin(Base):
    __tablename__ = 'user_login'

    id = Column(Integer, primary_key=True)
    email = Column(String(STRING_LEN_SMALL))
    password = Column(String(STRING_LEN_SMALL))
    phone = Column(String(LEN_MOBILE))
    is_verified = Column(Boolean, default=False)
    api_token = Column(String(STRING_LEN_LARGE))
    user_id = Column(Integer, ForeignKey('user.id'),nullable=True)
    user = relationship("User", backref=backref("user_login", uselist=False))
