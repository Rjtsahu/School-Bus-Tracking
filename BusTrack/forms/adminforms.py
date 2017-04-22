from flask_wtf import Form
from wtforms import StringField,PasswordField,SelectField
from wtforms.validators import DataRequired,Email
from BusTrack.helpers.validators import Unique
from BusTrack.models.driver import Driver

# admin login handle form
class UserPasswordForm(Form):
    username=StringField('username',validators=[DataRequired()])
    password=PasswordField('password',validators=[DataRequired()])

# add driver form
class AddDriverForm(Form):

    username = StringField('username', validators=[DataRequired(),
                                                   Unique(Driver,message='already exist')])
    password = PasswordField('password', validators=[DataRequired()])
    name=StringField('name',validators=[DataRequired()])
    contact=StringField('contact')  # add number validator later
    #--bus=SelectField('bus',choices=un_alloc) # not working

    '''
    jQuery sol'n for default select option
    $('.id_100 option').each(function() {
    if($(this).val() == 'val2') {
        $(this).prop("selected", true);
    }
    });
    '''

class AddKidForm(Form):
# add kid including parent detail
    parent_name=StringField('parent_name',validators=[DataRequired()])
    kid_name=StringField('kid_name',validators=[DataRequired()])
    email=StringField('email',validators=[DataRequired(),Email()])
    kid_section=StringField('kid_section')
    # bus_id: create custom select field