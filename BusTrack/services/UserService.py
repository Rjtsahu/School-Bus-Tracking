from BusTrack.repository import session
from BusTrack.repository.models.User import User

"""
Service to handle user related queries.
"""


class UserService:
    """
    Constructor with db injection for unit test.
    """

    def __init__(self, db=session):
        self.db = db

    """
    Get all user with given role.
    """

    def get_users_with_role(self, user_role):
        # use join instead
        return self.db.query(User).filter(User.user_role.role_name == user_role).all()

    # just for testing
    def get_all_user(self):
        return self.db.query(User).all()
