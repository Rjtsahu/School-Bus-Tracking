from flask import Blueprint, make_response, render_template, request, jsonify, abort, send_file
from BusTrack.models.Rides import ActiveRide, BusArriving, Track
from BusTrack.models.Parent import Parent
from BusTrack.helpers import SessionHelper, utils
from BusTrack.models.Kid import Kid
from BusTrack.models.feedback import Feedback
from functools import wraps

parent = Blueprint('parent', __name__)

# method to check valid parent and return access token
'''
request:
{
"username":"uname",
password:"pass"
}
response:
{
"status":"ok|error",
"message":"error type"
"token":"valid_till",
"name":"parent name",
"email","phone",
}
'''


@parent.route('/access_token', methods=['POST'])
def login():
    js = request.json
    if js is not None:
        if 'username' in js and 'password' in js:
            email = js['username']
            _pass = js['password']
            parent = Parent.get_user(email)
            if parent is None:
                return make_response(jsonify(status='error', message='invalid user'), 403)
            name = parent[1]
            phone = parent[3]
            pass_hash = parent[4]
            if pass_hash is not False and SessionHelper.is_password_correct(pass_hash, _pass):
                # ok correct user
                m_token = utils.rand(40)
                m_expire = utils.get_expiry_date_full()
                # update this token
                Parent.update_token(email, m_token, m_expire)
                return jsonify(status='ok', message='ok login', token=m_token, expires=m_expire, name=name, phone=phone,
                               email=email)
            else:
                return make_response(jsonify(status='error', message='invalid user'), 403)
        else:
            return jsonify(status='error', message='incorrect parameters')
    else:
        return jsonify(status='error', message='only json body is allowed')


# verify token
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' in request.args and Parent.is_valid_token(request.args['token']):
            pass
        else:
            return make_response(jsonify(status='error', message='unauthorized user'), 403)

        return f(*args, **kwargs)

    return decorated_function


# return kids detail of this parent
@parent.route('/get_kids', methods=['GET', 'POST'])
@token_required
def get_my_kids():
    return jsonify(kids=Parent.get_kids(request.args['token']), status='ok', message='ok')


# get all active ride for kids of this parent
@parent.route('/active_rides')
@token_required
def get_kid_status():
    try:
        r = ActiveRide(request.args['token'])
        if 'kid_id' in request.args:
            # request for only 1 kid
            # TODO: check only authorized parent, can access rides only for his kids
            kid_id = request.args['kid_id']
            return jsonify(rides=r.get_single_status(kid_id), status='ok', message='ok fetched')
        else:
            return jsonify(rides=r.get_active_ride(), status='ok', message='ok fetched')
    except:
        return make_response(jsonify(status='error'), 403)


# get all rides weather completed or incomplete associated to this kid
@parent.route('/recent_rides', methods=['GET', 'POST'])
@token_required
def get_recent_ride():
    # requires param kid_id
    if 'kid_id' in request.args:
        kid_id = request.args['kid_id']
        token = request.args['token']
        # if parent is authorised for this kid
        if not Parent.is_kidOf(kid_id, token):
            return make_response(jsonify(status='error', message='un-authorized access'), 403)
        try:
            a = ActiveRide(token)
            return jsonify(rides=a.get_recent_rides(kid_id), status='ok', message='fetched recent rides')
        except:
            return make_response(jsonify(status='error'), 403)
    else:
        return jsonify(status='error', message='incorrect request')


# fetch kid photo
@parent.route('/photo_kid')
@token_required
def get_kid_photo():
    if 'kid_id' in request.args:
        k_id = request.args['kid_id']
        token = request.args['token']
        img_name = Kid.get_image_for_parent(token, k_id)
        if img_name is None:
            abort(404)
        else:
            from BusTrack import app
            final_image = app.config['IMAGE_KID'] + img_name
            # import os
            # filename = os.path.join(app.root_path,img_name)
            try:
                return send_file(final_image, mimetype='image/jpeg')
            except:
                abort(404)
    else:
        abort(404)


# get feedback from parent
@parent.route('/feedback', methods=['POST'])
@token_required
def feedback():
    js = request.json
    if 'title' in js and 'detail' in js:
        token = request.args['token']
        title = js['title']
        detail = js['detail']
        date = utils.get_date_full()
        p = Parent.get_parent_id(token)
        p_id = p[0]
        name = p[1]
        email = p[2]
        f = Feedback(name=name, email=email, title=title, message=detail, date=date, p_id=p_id)
        f.add()
        return jsonify(status='ok', message='feedback sent')
    else:
        return jsonify(status='error', message='incorrect request')


# get list of arriving bus for the kids of this parent
@parent.route('/arriving', methods=['GET'])
@token_required
def arriving_bus():
    # if 'kid_id' in request.args:
    token = request.args['token']
    r = BusArriving(token)
    return jsonify(status='ok', buses=r.arriving_buses())


# get current gps status for bus
@parent.route('/location', methods=['GET', 'POST'])
@token_required
def latest_location():
    if 'kid_id' in request.args:
        token = request.args['token']
        kid_id = request.args['kid_id']
        t = Track(token, kid_id)
        res = t.get_latest_location()
        if res is None:
            return jsonify(status='completed', message='Ride already completed')
        else:
            return jsonify(status='ok', gps=res[0], last_update=res[1])
    else:
        return jsonify(status='error', message='incorrect parameters')


# get all location associated to a journey
@parent.route('/locations', methods=['GET'])
@token_required
def all_location():
    if 'kid_id' in request.args:
        kid_id = request.args['kid_id']
        token = request.args['token']
        t = Track(token, kid_id)
        res = t.get_all_locations()
        return jsonify(status='ok', locations=res)
    else:
        return jsonify(status='error', message='incorrect parameters')


# upload image of a kid
@parent.route('/upload',methods=['GET','POST'])
@token_required
def upload_image():
    token=request.args['token']
    if 'kid_id' in request.args and 'file' in request.files:
        kid_id=request.args['kid_id']
        image=request.files['file']
        file_name=image.filename
        image.save(file_name)

