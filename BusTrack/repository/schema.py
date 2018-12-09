# contains marshmallow schema models,which should be return as json output on api call
from BusTrack import ma
from marshmallow import fields as f


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('first_name', 'last_name', 'phone', 'address')


class UserLoginSchema(ma.Schema):
    class Meta:
        fields = ('email', 'phone', 'api_token', 'user_id')


class BasicBusSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'vehicle_number')


class KidProfileSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'section', 'photo', 'parent', 'bus')

    parent = f.Nested(UserSchema)
    bus = f.Nested(BasicBusSchema)


class KidsProfileSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'section', 'photo')


# prop to export
user_schema = UserSchema()
users_schema = UserSchema(many=True)

user_login_schema = UserLoginSchema()

kid_profile_schema = KidProfileSchema()

kids_profile_schema = KidsProfileSchema(many=True)
