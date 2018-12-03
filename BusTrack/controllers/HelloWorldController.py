from flask_restful import Resource
from flask import session
from BusTrack.services.UserService import UserService
from BusTrack.repository.schema import users_schema


class HelloWorldController(Resource):

    def get(self):
        # data = {'hello': 'world'}
        u = UserService()
        c = u.get_all_user()
        if 'user' not in session:
            session['user'] = {}
            session['user'] = {'a':'a'}# users_schema.jsonify(c)
        print('session',session['user'])
        return users_schema.jsonify(c)
