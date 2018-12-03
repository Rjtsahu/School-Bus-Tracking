from flask import make_response
from flask import request, session, abort
from BusTrack.services.UserLoginService import UserLoginService
from BusTrack.repository.schema import user_schema


# contains authorisation logic for apis

def token_required(role):
    def actual_function(f):
        def wrapper(*args, **kwargs):
            # main logic here
            login_service = UserLoginService()
            if 'auth_token' in request.headers and \
                    login_service.verify_token(request.args['auth_token'], role):
                # set user detail to this session
                session['user'] = user_schema.jsonify(login_service.user)
            else:
                return abort(401)

            return f(*args, **kwargs)

        return wrapper

    print('role is ', role)
    return actual_function
