from flask_restful import Resource
from flask import request,session
from BusTrack.services.UserLoginService import UserLoginService
from BusTrack.controllers import token_required

class UserLoginController(Resource):
    """"
    This API controller will handle user login logic for all roles.
    """

    def post(self):
        """
        This is post method for /login api to perform login,
        on success user session/token will be stored in database (planning to migrate to redis)
        :return success or failure status:
        """
        req = request.json
        user_login_service=UserLoginService(user=req)
        return user_login_service.perform_login()

    @token_required('Admin')
    def get(self):
        """
        get user detail from session
        :return user model:
        """
        user = session['user']
        return user