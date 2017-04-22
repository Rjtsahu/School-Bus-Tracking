from BusTrack import conn
from BusTrack.helpers import utils


class Location():
    __TABLE_ = 'location'

    def __init__(self, gps=None, journey_id=None):
        self.gps = gps
        self.time = utils.get_date_full()
        self.j_id = journey_id

    def add(self):
        cur = conn.execute('insert into location (gps,time,j_id) values(?,?,?) ',
                           (self.gps, self.time, self.j_id))
        conn.commit()
        return cur.lastrowid

    # return location point associated with a journey
    @staticmethod
    def get_location(journey_id):
        cur = conn.execute('select * from location where j_id=? ', [journey_id])

    # check if 1 minute passed since last_update
    @staticmethod
    def is_delta_time_passed(journey_id, prev_time):
        # if location have has no record
        cur=conn.execute(' select  max(id) from location where  j_id=?',[journey_id])
        res=cur.fetchone()
        if res[0] is None:
            return True # since first record
        else:
            cur = conn.execute(
                'select id from location where id=? and time(time)<time(?)',
                [res[0], prev_time])
            res = cur.fetchone()
            if res is None:
                return False
            else:
                return True
