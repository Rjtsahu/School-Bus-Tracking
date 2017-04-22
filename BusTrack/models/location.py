from BusTrack import conn
from BusTrack.helpers import utils
class Location():

    __TABLE_='location'

    def __init__(self,gps=None,journey_id=None):
        self.gps=gps
        self.time=utils.get_date_full()
        self.j_id=journey_id

    def add(self):
        cur=conn.execute('insert into location (gps,time,j_id) values(?,?,?) ',
                     (self.gps,self.time,self.j_id))
        conn.commit()
        return cur.lastrowid

    # return location point associated with a journey
    @staticmethod
    def get_location(journey_id):
        cur=conn.execute('select * from location where j_id=? ',(journey_id))