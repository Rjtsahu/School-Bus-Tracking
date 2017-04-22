from .. import conn
from BusTrack.models.Kid import Kid


class Attendance():
    __TABLE__ = 'attendance'

    def __init__(self, pick_present=0, drop_present=0, kid_id=None, journey_id=None, pick_gps=None, drop_gps=None,
                 pick_time=None, drop_time=None):
        # hold attendance for a kid for particular date
        self.k_id = kid_id
        # journey id
        self.j_id = journey_id
        # was kid present during picking
        self.pick_present = pick_present
        # was kid present during drop
        self.drop_present = drop_present
        self.pick_gps = pick_gps
        self.drop_gps = drop_gps
        self.pick_time = pick_time
        self.drop_time = drop_time

    def add(self):
        if self.k_id == None or self.j_id == None:
            assert 'Must provide kid and journey id'
        else:
            cur = conn.execute('insert into attendance (k_id,j_id,pick_present,drop_present,\
                               pick_gps,drop_gps,pick_time,drop_time) \
                                values(?,?,?,?,?,?,?,?)',
                               (self.k_id, self.j_id, self.pick_present, self.drop_present,
                                self.pick_gps, self.drop_gps, self.pick_time, self.drop_time))
            conn.commit()
            return cur.lastrowid

    #--------for pick up time in journey
    # return kids whose attendance is taken by driver for this journey
    @staticmethod
    def get_kid_attended(driver_token):
        cur = conn.execute('select * from kid  where kid.id  in ( \
            select attendance.k_id from attendance where attendance.j_id=( \
            select driver.active_ride_j_id  from driver where driver.token=? )) order by lower(kid.name) asc ', [driver_token])

        return Attendance.to_kid_list(cur.fetchall())

    # return kids whose attendance is not yet taken
    @staticmethod
    def get_kid_not_attended(driver_token):
        cur = conn.execute('select * from kid  where kid.id not in ( \
            select attendance.k_id from attendance where attendance.j_id=( \
            select driver.active_ride_j_id  from driver where driver.token=? )) \
             and kid.b_id=(select driver.b_id  from driver where driver.token=? ) order by lower(kid.name) asc', [driver_token,driver_token])
        return Attendance.to_kid_list(cur.fetchall())

    # ---------for drop time in journey
    #-----if the kid is picked but not yet dropped
    @staticmethod
    def get_kid_not_dropped(driver_token):
        cur=conn.execute('select * from kid  where kid.id  in ( \
        select attendance.k_id from attendance where attendance.j_id=( \
        select driver.active_ride_j_id  from driver where driver.token=? )\
        and attendance.drop_present=0  ) order by lower(kid.name) asc',[driver_token])
        return Attendance.to_kid_list(cur.fetchall())

    #-----get list of kid who is picked and also dropped
    @staticmethod
    def get_kid_dropped(driver_token):
        cur=conn.execute('select * from kid  where kid.id  in ( \
        select attendance.k_id from attendance where attendance.j_id=( \
        select driver.active_ride_j_id  from driver where driver.token=? )\
        and attendance.drop_present=1 ) order by lower(kid.name) asc ',[driver_token])
        return Attendance.to_kid_list(cur.fetchall())

    @staticmethod
    def to_kid_list(cursor):
        if cursor is None:
            return None
        kids = []
        for c in cursor:
            id = c[0]
            name = c[1]
            section = c[2]
            photo = c[3]
            kid = Kid(id=id, name=name, section=section, photo=photo)
            kids.append(kid)
        return kids

    # set dropped =1 to attendance table
    @staticmethod
    def update_drop_attendance(kid_id,drop_gps,drop_time,journey_id):
        cur=conn.execute('update attendance set drop_present=1,drop_gps=?,drop_time=? \
                         where k_id=? and j_id=? ',[drop_gps,drop_time,kid_id,journey_id])
        conn.commit()

