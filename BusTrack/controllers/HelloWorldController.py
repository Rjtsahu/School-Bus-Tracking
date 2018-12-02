from flask_restful import Resource
from flask import jsonify


class HelloWorldController(Resource):

    def get(self):
        data = {'hello': 'world'}
        return jsonify(data)
