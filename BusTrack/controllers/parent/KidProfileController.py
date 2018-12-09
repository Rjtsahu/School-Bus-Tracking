from flask_restful import Resource, reqparse
from BusTrack.controllers import token_required, get_user, Roles
from BusTrack.services.KidProfileService import KidProfileService

'''
parser = reqparse.RequestParser()
parser.add_argument('param1')
parser.add_argument('param2')
args = parser.parse_args()
'''


class KidProfileController(Resource):

    @token_required([Roles.PARENT])
    def get(self, kid_id=None):

        kid_profile_service = KidProfileService()
        current_user = get_user()

        if kid_id is None:
            # select all kids associated to this parent
            result = kid_profile_service.get_kids_for_parent(current_user['user_id'])
        else:
            result = kid_profile_service.get(kid_id, current_user['user_id'])

        if result is None:
            return {'status': 'ok', 'message': 'No record found', 'data': result}
        else:
            return {'status': 'ok', 'data': result}
