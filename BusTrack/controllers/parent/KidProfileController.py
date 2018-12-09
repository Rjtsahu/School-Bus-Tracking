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
        if kid_id is None:
            # select all kids associated to this parent
            pass
        else:
            kid_profile_service = KidProfileService()
            return kid_profile_service.get(kid_id)
        data = {'hello': 'in KidProfileController'}
        return data
