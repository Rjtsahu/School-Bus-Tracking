# contains marshmallow schema models,which should be return as json output on api call
from BusTrack import ma


class Schemas:
    """
    Class to hides multiple schemas,or simple a holder class for all schemas.
    """

    class UserSchema(ma.Schema):
        class Meta:
            # Fields to expose
            fields = ('first_name', 'last_name', 'phone','address')


# prop to export
user_schema = Schemas.UserSchema()
users_schema = Schemas.UserSchema(many=True)