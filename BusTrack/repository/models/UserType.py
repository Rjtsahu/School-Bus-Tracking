from sqlalchemy import Column, String, Integer
from BusTrack.repository import Base, session


class UserType(Base):
    __tablename__ = 'user_type'

    id = Column(Integer, primary_key=True)
    role_name = Column(String(100))

    @staticmethod
    def __create_default_role__():
        if session.query(UserType).count() != 0:
            return
        driver = UserType()
        driver.role_name = 'Driver'
        parent = UserType()
        parent.role_name = 'Parent'
        admin = UserType()
        admin.role_name = 'Admin'

        session.add(driver)
        session.add(parent)
        session.add(admin)

        session.commit()
        session.close()
