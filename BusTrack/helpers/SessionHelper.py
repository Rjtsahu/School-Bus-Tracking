from flask import session
from BusTrack import bcrypt

ADMIN_LOGIN = 'is_admin_login'
ADMIN_LOGIN_ID = 'admin_id'
TOKEN='token'

def nav_list():
    # items to show in navigation list
    nav_logged_in = [('/admin/', 'Home'), ('/admin/driver', 'Add Update Driver'),
                     ('/admin/student', 'Add Kid'), ('/admin/track', 'Track'),
                     ('/admin/feedback', 'Feedback'), ('/admin/logout', 'Logout')]
    nav_logged_out = [('/admin/', 'Home'), ('/admin/login', 'Login')]

    if is_login_admin():
        return nav_logged_in
    else:
        return nav_logged_out


def is_login_admin():
    # check login session of admin
    if ADMIN_LOGIN in session:
        if session[ADMIN_LOGIN] == True:
            return True
    else:
        return False


def get_password_hash(password):
    return bcrypt.generate_password_hash(password)


def is_password_correct(pass_hash, password):
    # return true if correct
    return bcrypt.check_password_hash(pass_hash, password)

