from flask import Blueprint, jsonify
from BusTrack.services.UserLoginService import UserLoginService
from BusTrack.services.UserService import UserService

userLoginController = Blueprint('controller', __name__)


@userLoginController.route('/test', methods=['GET'])
def test_service():
    uls = UserLoginService()
    a=uls.get_user_with_token('testtest')
    b=uls.verify_token('testtest', 'Admin')
    u=UserService()
    c=u.get_users_with_role('')
    return jsonify(c)
