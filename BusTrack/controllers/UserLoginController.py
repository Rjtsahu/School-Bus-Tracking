from flask_restful import Resource
from flask import request, Response, jsonify
from BusTrack.services.UserService import UserService
from BusTrack.services.UserLoginService import UserLoginService
from BusTrack.repository.schema import user_schema, users_schema


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

