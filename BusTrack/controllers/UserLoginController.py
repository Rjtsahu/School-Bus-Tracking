from flask_restful import Resource
from BusTrack.services.UserService import UserService
from BusTrack.services.UserLoginService import UserLoginService
from BusTrack.repository.schema import user_schema, users_schema


class UserLoginController(Resource):

    def get(self):
        userLoginService = UserLoginService()
        a = userLoginService.get_user_with_token('testtest')
        b = userLoginService.verify_token('testtest', 'Admin')
        u = UserService()
        c = u.get_users_with_role('')

        return users_schema.jsonify(c)
