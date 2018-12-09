from BusTrack.repository import session
from BusTrack.repository.models.User import User
from BusTrack.repository.models.Kid import Kid
from BusTrack.repository.schema import kid_profile_schema

"""
Service to handle user related queries.
"""


class KidProfileService:
    """
    Constructor with db injection for unit test.
    """

    def __init__(self, db=session):
        self.db = db

    def get(self, kid_id):
        """
        Get kid with given kid_id .
        :return kid model
        """
        kid = self.db.query(Kid).filter(Kid.id == kid_id).first()
        if kid == None:
            return
        return kid_profile_schema.jsonify(kid)

