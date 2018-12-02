from flask_restful import Resource
from BusTrack.services.UserService import UserService
from BusTrack.repository.schema import user_schema, users_schema


class HelloWorldController(Resource):

    def get(self):
        # data = {'hello': 'world'}
        u = UserService()
        c = u.get_all_user()
        return users_schema.jsonify(c)
