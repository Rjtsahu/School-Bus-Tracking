from BusTrack.helpers import utils
from BusTrack.models.Parent import Parent
from BusTrack import conn


# a special file to handle Rides related stuff
# fetch ride of all kids of a parent
# parent token require
class ActiveRide():
    def __init__(self, token, date=utils.get_date_only()):
        if token is None or token is '':
            raise ValueError('invalid token')  # error 403
        self.token = token
        self.date = date  # default today if not provided
        self.is_active = True

    # get active ride for each kid
    def get_active_ride(self):
        kids = Parent.get_kids(self.token)  # may be None
        if kids is None:
            raise ValueError('invalid token')  # error 403

        rides = []
        for kid_bus in kids:
            kid = kid_bus['kid']
            res = self.__sql__(kid['id'])
            if res is not None:
                rides.append({"kid": kid, "journey_id": res[0], "journey_type": res[1], "current_gps": res[2],
                              "start_time": res[3], "start_gps": res[4]})
        return rides

    # return single kid status , weather today's ride is completed or active
    def get_single_status(self, kid_id):
        res = self.__sql__(kid_id)
        if res is None:
            return 'no active ride'  # no active
        else:
            return 'ride is active '  # yes active


    def __sql__(self, kid_id):
        cur = conn.execute('select  journey.id,journey.j_type ,journey.gps,attendance.pick_time,\
               attendance.pick_gps from attendance inner join journey on attendance.j_id=journey.id \
               where date(attendance.pick_time)=date(?) and attendance.k_id=? \
               and attendance.drop_present=0 limit 1 ', [self.date, kid_id])
        return cur.fetchone()


    # get all recent rides associated to this kid
    def get_recent_rides(self, kid_id):
        cur = conn.execute('select  journey.id,journey.j_type ,attendance.pick_time,'
                           'attendance.pick_gps ,attendance.drop_time,attendance.drop_gps,attendance.drop_present , journey.gps '
                           'from attendance inner join journey on attendance.j_id=journey.id '
                           'where attendance.k_id=?  order by attendance.id desc limit 50 ', [kid_id])
        res = cur.fetchall()
        if res is None:
            return []
        else:
            l = []
            for r in res:
                l.append(
                    {"journey_id": r[0], "journey_type": r[1], "start_time": r[2], "start_gps": r[3], "end_time": r[4],
                     "end_gps": r[5], "completed": r[6],"current_gps":r[7]})
            return l


# a special class to handle bus status
# check the bus current location if it is to be arrived kid's home
# scenario:
# * Bus driver login  to app when driver to pick student from their home to school
# * SO here journey_type=0 (from home to school)
# * now check in attendance table weather kid is already picked up, if not then
# * show bus status as arriving (send current location and distance)

class BusArriving():
    def __init__(self, token):
        self.token = token
        if token is None or token is '':
            raise ValueError('Invalid Token')

    # return a str message about bus arriving status
    def arriving_buses(self):
        kids = Parent.get_kids(self.token)
        # iterate for each kid
        arr = []
        for k in kids:
            k_id = k['kid']['id']
            b_id = k['bus']['bus_id']
            res = self.__get_journey__(k_id, b_id)
            if res is not None:
                res['name'] = k['kid']['name']
                arr.append(res)
        return arr

    # gets journey detail of arriving bus , for this bus on active ride
    def __get_journey__(self, kid_id, bus_id):
        cur = conn.execute(
            'select journey.id,journey.gps,journey.last_update from journey inner join driver on '
            'journey.id=driver.active_ride_j_id '
            ' where driver.b_id=? and j_type=0 ',
            [bus_id])
        res = cur.fetchone()
        if res is None:
            # no journey exist
            return None
        else:
            cur = conn.execute('select id from attendance where k_id=? and j_id=? ', [kid_id, res[0]])
            res_2 = cur.fetchone()
            # if exist NO record, it means kid is still waiting for bus
            if res_2 is None:
                return {"id": res[0], "current_gps": res[1], "last_update": res[2], "bus_id": bus_id, "kid_id": kid_id}
            else:
                # kids journey is already started
                return None

    # check if bus is arriving for this kid
    def arriving_for_kid(self, kid_id, bus_id):
        res = self.__get_journey__(kid_id, bus_id)
        if res is None:
            return False
        else:
            return res


class Track:
    def __init__(self, p_token, kid_id):
        self.token = p_token
        self.kid_id = kid_id

    # get current location of bus
    def get_latest_location(self):
        cur = conn.execute('select journey.gps,journey.last_update from journey where journey.id= ( '
                           'select driver.active_ride_j_id from driver inner join kid on kid.b_id=driver.b_id '
                           'inner join parent on parent.id=kid.p_id where parent.token=? and kid.id=? ) and '
                           'journey.end=0',
                           [self.token, self.kid_id])
        return cur.fetchone()

    # get all location in this journey
    def get_all_locations(self):
        cur = conn.execute('select location.id,location.gps,location.time from location where location.j_id= ( '
                           ' select driver.active_ride_j_id from driver inner join kid on kid.b_id=driver.b_id '
                           'inner join parent on parent.id=kid.p_id where parent.token=? and kid.id=? ) order by '
                           'location.id desc limit 100',
                           [self.token, self.kid_id])
        res = cur.fetchall()
        if res is None:
            return []
        else:
            return [{"id":i[0],"gps": i[1], "time": i[2]} for i in res]
