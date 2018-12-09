from flask import Blueprint, render_template, jsonify, redirect, url_for, request, flash
from flask import session
from functools import wraps
from BusTrack.helpers import SessionHelper, utils
from BusTrack.forms.adminforms import UserPasswordForm, AddDriverForm, AddKidForm
from BusTrack.models.driver import Driver
from BusTrack.models.bus import Bus
from BusTrack.models.Kid import Kid
from BusTrack.models.Parent import Parent
from BusTrack.models.feedback import Feedback

admin = Blueprint('admin', __name__)


# custom decorator to handle access
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'is_admin_login' in session:
            if session['is_admin_login'] == True:
                pass  # ok no problem
            else:
                return redirect(url_for('admin.login', next=request.url))
        else:
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@admin.route('/')
def root():
    return render_template('admin/index.html')


@admin.route('/index')
def index():
    return render_template('admin/index.html')


@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = UserPasswordForm(request.form)
    if form.validate_on_submit() and request.method == 'POST':
        # check password and redirect to admin home
        from BusTrack import app
        if app.config['ADMIN_USERNAME'] == form.username.data and \
                SessionHelper.is_password_correct(app.config['ADMIN_PASSWORD'], form.password.data):
            session['is_admin_login'] = True
            return redirect(request.args.get('next') or url_for('admin.index'))
        else:
            flash('incorrect credentials')
            render_template('admin/login.html', form=form)

    return render_template('admin/login.html', form=form)


@admin.route('/driver', methods=['POST', 'GET'])
@login_required
def driver():
    # handle driver tasks
    form = AddDriverForm(request.form)
    # TODO : Disable add when no bus unallocated (for now using front-end logic)
    un_alloc = Bus.unallocated_bus()
    if form.validate_on_submit() and request.method == 'POST':
        # if 'bus' not in request.form:

        # TODO: later add option for update
        d = Driver(user_id=form.username.data, bus_id=request.form['bus']
                   , name=form.name.data, contact=form.contact.data,
                   password=SessionHelper.get_password_hash(form.password.data))
        d.add()
        # clear fileds
        form.username.data = form.name.data = form.contact.data = ''
        # return render_template('admin/driver.html',form=form)
    alloc_driver = Driver.get_all_allocated()
    return render_template('admin/driver.html', form=form, bus_data=un_alloc, driver_list=alloc_driver)


@admin.route('/kid', methods=['GET', 'POST'])
@login_required
def kid():
    form = AddKidForm(request.form)

    if form.validate_on_submit() and request.method == 'POST':
        if 'bus' in request.form:
            rand_pass = utils.rand(6)
            # store parent and get its unique id to store it in Kid table
            # BUT BUT ,if parent already register then don't re-register instead add this kid to previously added parent
            p = Parent(name=form.parent_name.data, password=rand_pass, email=form.email.data)
            p_id = p.add_or_get()
            k = Kid(name=form.kid_name.data, section=form.kid_section.data, bus_id=request.form['bus'], parent_id=p_id)
            from sqlite3 import IntegrityError
            k.add()
            # clear form field
            form.parent_name.data = form.email.data = form.kid_name.data = form.kid_section.data = form.parent_name.data = ''
            # TODO: Send this generated password to Parent email

        else:
            all_parent_kid = Parent.get_all_parent_kid_with_bus()
            all_bus = Bus().get_all()
            return render_template('admin/kid.html', form=form, bus_data=all_bus, bus_error='Must Select a Bus',
                                   all_parent_kid=all_parent_kid)
    all_parent_kid = Parent.get_all_parent_kid_with_bus()
    all_bus = Bus().get_all()
    return render_template('admin/kid.html', form=form, bus_data=all_bus, all_parent_kid=all_parent_kid)


@admin.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    feed = Feedback().get_all()
    return render_template('admin/feeds.html', feed_list=feed)


@admin.route('/track', methods=['GET', 'POST'])
@login_required
def show_map():
    if request.method == 'GET':
        print("get method")
    elif request.method == 'POST':
        print("post method")
    return render_template('/admin/track.html')


@admin.route('/api/reply_email', methods=['POST'])
@login_required
def reply_email():
    # get data as post
    if 'msg_id' in request.form and 'email' in request.form and 'title' in request.form and 'message' in request.form:
        # TODO send email using smtp api
        return jsonify(success='ok', message='message sent')
    else:
        return jsonify(success='error', message='insufficient parameters')


@admin.route('/logout')
def logout():
    session.pop('is_admin_login', None)
    return redirect(url_for('admin.login'))
