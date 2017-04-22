from flask import Blueprint, make_response,render_template, request, jsonify
from BusTrack.models.Parent import Parent
from BusTrack.helpers import SessionHelper, utils
from functools import wraps

parent = Blueprint('parent', __name__)

# method to check valid parent and return access token
'''
request:
{
"username":"uname",
password:"pass"
}
response:
{
"status":"ok|error",
"message":"error type"
"token":"valid_till",
"name":"parent name",
"email","phone",
}
'''


@parent.route('/access_token', methods=['POST'])
def login():
    js = request.json
    if js is not None:
        if 'username' in js and 'password' in js:
            email = js['username']
            _pass = js['password']
            parent = Parent.get_user(email)
            if parent is None:
                return make_response(jsonify(status='error', message='invalid user'),403)
            name = parent[1]
            phone = parent[3]
            pass_hash = parent[4]
            if pass_hash is not False and SessionHelper.is_password_correct(pass_hash, _pass):
                # ok correct user
                m_token = utils.rand(40)
                m_expire = utils.get_expiry_date_full()
                # update this token
                Parent.update_token(email, m_token, m_expire)
                return jsonify(status='ok', message='ok login', token=m_token, expires=m_expire, name=name, phone=phone,email=email)
            else:
                return make_response(jsonify(status='error', message='invalid user'),403)
        else:
            return jsonify(status='error', message='incorrect parameters')
    else:
        return jsonify(status='error', message='only json body is allowd')

# verify token
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' in request.args and Parent.is_valid_token(request.args['token']):
            pass
        else:
            return make_response(jsonify(status='error', message='unauthorized user'),403)

        return f(*args, **kwargs)

    return decorated_function

# return kids detail of this parent
@parent.route('/get_kids',methods=['GET','POST'])
@token_required
def get_my_kids():
    return jsonify(kids=Parent.get_kids(request.args['token']))

