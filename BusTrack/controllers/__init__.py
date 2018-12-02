from functools import wraps

from flask import Blueprint, make_response, request, jsonify

from BusTrack.models.Parent import Parent



# verify token
def token_required(f,role):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' in request.args and Parent.is_valid_token(request.args['token']):
            pass
        else:
            return make_response(jsonify(status='error', message='unauthorized user'), 403)

        return f(*args, **kwargs)

    return decorated_function
