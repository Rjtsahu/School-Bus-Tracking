from BusTrack.repository import session
from BusTrack.repository.models.UserLogin import UserLogin
from BusTrack.helpers.utils import rand

"""
Service to handle user related queries.
"""


class UserLoginService:
    """
    Constructor with db injection for unit test.
    """

    def __init__(self, user=None, db=session):
        self.user = user
        self.db = db

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

    """
    Get user associated with given credentials
    """

    def get_user(self):
        if self.user is None:
            raise ValueError("user object is null,pass it on class constructor.")
        return self.db.query(UserLogin).filter(
            UserLogin.email == self.user['username']) \
            .filter(UserLogin.password == self.user['password']).first()

    """
    Main method to be called that handles login logic
    """

    def perform_login(self):
        if self.user is None:
            raise ValueError("user object is null,pass it on class constructor.")

        if 'username' not in self.user or 'password' not in self.user:
            return {'status': 'error', 'message': 'must provide username and password in request json body.'}
        user = self.get_user()
        if user is None:
            return {'status': 'error', 'message': 'Invalid credentials.'}
        # create new api token and update for this user
        user.api_token = rand(40)
        session.commit()
        return {'status': 'ok', 'email': user.email, 'phone': user.phone, 'token': user.api_token}
