from flask_wtf import Form
from wtforms import StringField,PasswordField,SelectField
from wtforms.validators import DataRequired,Email
from BusTrack.helpers.validators import Unique
from BusTrack.models.driver import Driver

'''
Forms to be used in ADMIN web pages 
'''

# Form for /admin/login
class UserPasswordForm(Form):
    username=StringField('username',validators=[DataRequired()])
    password=PasswordField('password',validators=[DataRequired()])

# form for /admin/driver
class AddDriverForm(Form):
    username = StringField('username', validators=[DataRequired(),
                                                   Unique(Driver,message='already exist')])
    password = PasswordField('password', validators=[DataRequired()])
    name=StringField('name',validators=[DataRequired()])
    contact=StringField('contact')  # TODO: add phone number validator
    
# form for /admin/kid
class AddKidForm(Form):
    parent_name=StringField('parent_name',validators=[DataRequired()])
    kid_name=StringField('kid_name',validators=[DataRequired()])
    email=StringField('email',validators=[DataRequired(),Email()])
    kid_section=StringField('kid_section')
    
