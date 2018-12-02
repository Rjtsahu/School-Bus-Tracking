from BusTrack.repository import session
from BusTrack.repository.models.UserLogin import UserLogin

"""
Service to handle user related queries.
"""


class UserLoginService:
    """
    Constructor with db injection for unit test.
    """

    def __init__(self, db=session):
        self.db = db
        self.user = None

    """
    Method to verify that token is valid for given role.
    In case token is valid it will set self.user as the user representing token.
    """

    def verify_token(self, token, role):
        user_login = self.get_user_with_token(token)
        if user_login is None or user_login.user is None or user_login.user.user_role.role_name != role:
            return False
        self.user = user_login
        return True

    """
    Get user with given api token
    """

    def get_user_with_token(self, token):
        return self.db.query(UserLogin).filter(UserLogin.api_token == token).first()
