from flask import request, session, abort
from BusTrack.services.UserLoginService import UserLoginService
from BusTrack.repository.schema import user_login_schema
import BusTrack.helpers.JsonHelper as JsonHelper


class Roles:
    ADMIN = 'Admin'
    PARENT = 'Parent'
    DRIVER = 'Driver'


# contains authorisation logic for apis

def token_required(roles):
    def actual_function(f):
        def wrapper(*args, **kwargs):
            # main logic here
            login_service = UserLoginService()
            if 'auth_token' in request.headers and \
                    login_service.verify_token(request.headers['auth_token'], roles):
                # set user detail to this session
                session['user'] = JsonHelper.to_json_serializable(user_login_schema, login_service.user)
            else:
                return abort(401)

            return f(*args, **kwargs)

        return wrapper

    if type(roles) != list:
        raise TypeError("roles must contains list of role from Roles class.")
    return actual_function


def get_user():
    if 'user' in session:
        return session['user']


def remove_user():
    del session['user']
