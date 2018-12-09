from flask_restful import Api
from flask import Blueprint
from BusTrack.controllers.HelloWorldController import HelloWorldController
from BusTrack.controllers.UserLoginController import UserLoginController
from BusTrack.controllers.parent import register_controllers as register_controllers_parent


def register_rest_api(app):
    rest_api = Blueprint('api', __name__)
    api = Api(rest_api)  # rest api using flask_restful extension
    app.register_blueprint(rest_api, url_prefix='/api/v1')
    register_controllers(api)


def register_controllers(api):
    api.add_resource(HelloWorldController, '/hello')
    api.add_resource(UserLoginController, '/login')
    register_controllers_parent(api, '/parent')
