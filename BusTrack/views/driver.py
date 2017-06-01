from flask import Blueprint, make_response, request, jsonify, abort, send_file, send_from_directory
from BusTrack.models.driver import Driver
from BusTrack.models.journey import Journey
from BusTrack.models.gps import Gps
from BusTrack.models.attendance import Attendance
from BusTrack.models.location import Location
from BusTrack.models.Kid import Kid
from  BusTrack.helpers import SessionHelper, utils
from functools import wraps

driver = Blueprint('driver', __name__)

# method to check valid driver and return access token to be used by him
'''
# request object
{
username:"username",
password:"password"
}

# response object
{
status:"ok|error"
valid_till:"duration of expiry",
token:"send generated access token",
name:"name of driver",
bus:"bus number"
message:"String message responding  status related to success or failure."
}
'''


@driver.route('/access_token', methods=['POST'])
def login():
    # require username,password as json
    js = request.json
    if js is not None:
        if 'username' in js and 'password' in js and 'journey_type' in js:
            u_id = js['username']
            _pass = js['password']
            j_type = js['journey_type']
            # validate j_type
            if j_type not in [0, 1]:
                return jsonify(status="error", message="Incorrect journey type")

            user = Driver.get_user(u_id)
            if not user:
                return make_response(jsonify(status='error', message='Invalid Credential'), 403)
            name = user[0]
            pass_hash = user[1]
            bus_no = user[2]

            if pass_hash is not False and SessionHelper.is_password_correct(pass_hash, _pass):
                # ok correct user
                # make sure, if similar ride is not already completed by this driver
                if Driver.is_ride_already_completed(u_id, j_type):
                    return jsonify(status='error', message='ride already completed for today.')
                # get active ride
                active_ride = user[3]
                #  generate a random token
                m_token = utils.rand(40)
                m_expire = utils.get_expiry_date_full()
                Driver.update_token(m_token, m_expire, u_id)
                if active_ride is None or active_ride is '':
                    # no active session, start new session
                    # and create new journey and set it
                    bus_id = user[4]
                    Journey.trans_create_journey(j_type, utils.get_date_full(), bus_id, u_id)
                else:
                    # no need  to create new journey
                    pass
                return jsonify(status="ok", message="Correct Credentials", token=m_token, valid_till=m_expire,
                               name=name, bus=bus_no)
            else:
                return make_response(jsonify(status="error", message="Invalid Credential"), 403)
        else:
            return jsonify(status="error", message="Incorrect Request")
    else:
        return jsonify(status="error", message="Only Json Body is allowed")

        # - a decorator to check validity of token


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' in request.args and Driver.is_valid_token(request.args['token']):
            pass
        else:
            return make_response(jsonify(status='error', message='unauthorized user'), 403)

        return f(*args, **kwargs)

    return decorated_function


# add gps data of this driver
'''
#request object
..api/v1/driver/add_gps?token="mToken"
{
lat:"latitude",
lon:"longitude",
}

# response object
{
status:"ok|error",
message:"error message if any"
}
'''


@driver.route('/add_gps', methods=['POST'])
@token_required
def add_gps():
    js = request.json
    if 'lat' in js and 'lon' in js:
        token = request.args['token']
        lat = js['lat']
        lon = js['lon']
        # add location to this active journey
        print(lat, lon)
        j_id = Driver.get_active_ride(request.args['token'])
        if j_id is None or j_id is '':
            return jsonify(status='error', message='unauthorized user or inactive session')
        else:
            # add location to location table
            # check if 1 minute passed since last update
            if Location.is_delta_time_passed(j_id, utils.get_prev_time()):
                # now add location
                l = Location(Gps.tuple_to_str(lat, lon), j_id)
                l.add()
                print("adding location...")
            # update gps table
            Journey.update_gps(j_id, Gps.tuple_to_str(lat, lon))

            return jsonify(status="ok", message="Gps data added")
    else:
        return jsonify(status='error', message='Incorrect parameters')


# logout for driver
@driver.route('/logout', methods=['GET', 'POST'])
@token_required
def logout():
    # set this journey_id to null for this driver
    # and also set end time
    token = request.args['token']
    # check all attendance stuff are already done by driver
    Driver.logout_session(token)
    return jsonify(status='ok')


# get list of kids in bus at pick time
# 1) list of kids whose attendance is already taken ?present=1
# 2) list of kids whom attendance is not yet taken  ?present=0
@driver.route('/get_kids', methods=['GET', 'POST'])
@token_required
def get_kids():
    if 'present' in request.args:
        # but make sure a ride session exists
        j_id = Driver.get_active_ride(request.args['token'])
        if j_id is None or j_id is '':
            return jsonify(status='error', message='No active ride.')
        present = request.args['present']
        token = request.args['token']
        if present is '1' or present is 1:
            kids = Attendance.get_kid_attended(token)
            return jsonify(status='ok', kids=kids_json(kids))
        elif present is '0' or present is 0:
            kids = Attendance.get_kid_not_attended(token)
            return jsonify(status='ok', kids=kids_json(kids))
        else:
            return jsonify(status='error', message='present arg can be 0 or 1')
    else:
        return jsonify(status='error', message='incorrect request')


# get list of kids at drop time
# 1) kids who are not yet dropped ?dropped=0
# 2) kids who are already dropped ?dropped=1
@driver.route('/get_kids_dropped', methods=['GET', 'POST'])
@token_required
def get_kids_by_dropping():
    if 'dropped' in request.args:
        # but make sure a ride session exists
        j_id = Driver.get_active_ride(request.args['token'])
        if j_id is None or j_id is '':
            return jsonify(status='error', message='No active ride.')
        dropped = request.args['dropped']
        token = request.args['token']
        if dropped is '1' or dropped is 1:
            kids = Attendance.get_kid_dropped(token)
            return jsonify(status='ok', kids=kids_json(kids))
        elif dropped is '0' or dropped is 0:
            kids = Attendance.get_kid_not_dropped(token)
            return jsonify(status='ok', kids=kids_json(kids))
        else:
            return jsonify(status='error', message='present arg can be 0 or 1')
    else:
        return jsonify(status='error', message='incorrect request')


# make attendance function
# for pick up
'''
--request format
{
"kid_ids":[1,2,3,4,...],
"lat":12.5,
 "lon":53.254
 }
 # send ids of kid
--response
"status":"ok","message":"msg.."
'''


@driver.route('/add_pick_attendance', methods=['POST'])
def pick_attendance():
    js = request.json
    if 'kid_ids' in js and 'lat' in js and 'lon' in js:
        ids = js['kid_ids']
        lat = js['lat']
        lon = js['lon']
        gps = Gps.tuple_to_str(lat, lon)
        time = utils.get_date_full()
        token = request.args['token']
        j_id = Driver.get_active_ride(token)
        if j_id is None or j_id is '':
            return jsonify(status='error', message='Cant add,as not active ride')
        else:
            # filter valid ids
            id_from_db = Kid.get_kid_ids(j_id)
            ids_set = set(ids)
            ids_db_set = set(id_from_db)
            ids_valid = list(ids_set & ids_db_set)  # intersection of kid ids
            for id in ids_valid:
                atten = Attendance(pick_present=1, kid_id=id, journey_id=j_id, pick_gps=gps, pick_time=time)
                atten.add()
            return jsonify(status='ok', message='Attendance taken')
    else:
        return jsonify(status='error', message='incorrect request')


@driver.route('/add_drop_attendance', methods=['POST'])
def drop_attendance():
    js = request.json
    if 'kid_ids' in js and 'lat' in js and 'lon' in js:
        ids = js['kid_ids']
        lat = js['lat']
        lon = js['lon']
        gps = Gps.tuple_to_str(lat, lon)
        time = utils.get_date_full()
        token = request.args['token']
        j_id = Driver.get_active_ride(token)
        if j_id is None or j_id is '':
            return jsonify(status='error', message='Cant add,since not active ride')
        else:
            # filter valid ids
            id_from_db = Kid.get_kid_drop_not_present(j_id)
            ids_set = set(ids)
            ids_db_set = set(id_from_db)
            ids_valid = list(ids_set & ids_db_set)  # intersection of kid ids
            for id in ids_valid:
                Attendance.update_drop_attendance(id, gps, time, j_id)
            return jsonify(status='ok', message='Attendance taken')
    else:
        return jsonify(status='error', message='incorrect request')


# convert kids list to json compatible dictionary-list
def kids_json(kids):
    lst = []
    for k in kids:
        dic = {'name': k.name, 'section': k.section, 'id': k.id}
        # TODO: create logic to create image link
        # dic['photo']
        lst.append(dic)
    return lst


@driver.route('/photo_kid')
@token_required
def get_kid_photo():
    if 'kid_id' in request.args:
        k_id = request.args['kid_id']
        token = request.args['token']
        img_name = Kid.get_image_for_driver(token, k_id)
        if img_name is None:
            abort(404)
        else:
            from BusTrack import app
            final_image = app.config['IMAGE_KID'] + img_name
            try:
                return send_file(final_image, mimetype='image/jpeg')
            except:
                abort(404)
    else:
        abort(404)


# get information about ride completed  by this driver
'''
request:get_rides?token=xyz...

response:
{
"rides":[{
"start_time":"time","end_time":"time","duration":"calculate it on front end",
"type":"1 or 0",

},..]
}
'''
