from BusTrack.repository import session
from BusTrack.repository.models.User import User
from BusTrack.repository.models.Kid import Kid
from BusTrack.repository.schema import kid_profile_schema, kids_profile_schema
import BusTrack.helpers.JsonHelper as JsonHelper


class KidProfileService:
    """
    Service to handle kids related queries.
    """

    def __init__(self, db=session):
        self.db = db

    def get(self, kid_id, parent_id=None):
        """
        Get kid with given kid_id and associated parent_id.
        :return kid model.
        """
        kid = self.db.query(Kid).filter(Kid.id == kid_id).first()
        if kid is None:
            return
        if parent_id is None or kid.parent.id == parent_id:
            return JsonHelper.to_json_serializable(kid_profile_schema, kid)

    def get_kids_for_parent(self, parent_id):
        """
        Get all kids associated to a parent
        :param parent_id: parent user_id
        :return: list of models.
        """
        user = self.db.query(User).filter(User.id == parent_id).first()
        if user is None or user.kids is None:
            return
        return JsonHelper.to_json_serializable(kids_profile_schema, user.kids)
