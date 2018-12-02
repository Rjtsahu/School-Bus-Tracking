from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from datetime import datetime
from BusTrack.repository import Base
from BusTrack.repository.models import STRING_LEN_SMALL, STRING_LEN_MEDIUM, STRING_LEN_LARGE, LEN_MOBILE


class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True)
    name = Column(String(STRING_LEN_SMALL))
    email = Column(String(STRING_LEN_SMALL))
    title = Column(String(STRING_LEN_MEDIUM))
    message = Column(String(STRING_LEN_LARGE))
    date = Column(DateTime, default=datetime.utcnow())
    user_id = Column(ForeignKey('user.id'), default=None)
