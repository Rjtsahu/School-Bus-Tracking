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

    def verify_token(self, token, roles):
        """
         Method to verify that token is valid for given role.
         In case token is valid it will set self.user as the user representing token.
         """

        user_login = self.get_user_with_token(token)
        if user_login is None or user_login.user is None or user_login.user.user_role.role_name not in roles:
            return False
        self.user = user_login
        return True

    def get_user_with_token(self, token):
        """
        Get user with given api token
        """

        return self.db.query(UserLogin).filter(UserLogin.api_token == token).first()

    def get_user(self):
        """
        Get user associated with given credentials
        """

        if self.user is None:
            raise ValueError("user object is null,pass it on class constructor.")
        return self.db.query(UserLogin).filter(
            UserLogin.email == self.user['username']) \
            .filter(UserLogin.password == self.user['password']).first()

    def remove_token(self, token):
        """
        Updates token in user_login table to null
        :param token: api token used in auth
        :return: None
        """
        record = self.db.query(UserLogin).filter(UserLogin.api_token == token).first()
        record.api_token = ''
        self.db.commit()

    def perform_login(self):
        """
        Main method to be called that handles login logic
        """

        if self.user is None:
            raise ValueError("user object is null,pass it on class constructor.")

        if 'username' not in self.user or 'password' not in self.user:
            return {'status': 'error', 'message': 'must provide username and password in request json body.'}
        user = self.get_user()
        if user is None:
            return {'status': 'error', 'message': 'Invalid credentials.'}
        # create new api token and update for this user
        user.api_token = rand(40)
        self.db.commit()
        return {'status': 'ok', 'email': user.email, 'phone': user.phone, 'token': user.api_token}
