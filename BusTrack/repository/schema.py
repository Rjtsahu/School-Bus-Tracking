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


class KidProfileSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'section', 'photo', 'parent')
    parent = f.Nested(UserSchema)


# prop to export
user_schema = UserSchema()
users_schema = UserSchema(many=True)

user_login_schema = UserLoginSchema()

kid_profile_schema = KidProfileSchema()
kids_profile_schema = KidProfileSchema(many=True)
