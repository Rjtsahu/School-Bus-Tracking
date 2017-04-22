from BusTrack import conn
from BusTrack.helpers import utils


class Journey():
    __TABLE__ = 'journey'

    def __init__(self, board=0, start=None, end=None, gps=None, bus_id=None):
        self.b_id = bus_id
        # board boolean:true = 'home to school', false:'school to home'
        self.board = board
        self.date = utils.get_date_full()
        self.start = start  # start time
        self.end = end  # end time of journey
        self.gps = gps  # current gps information (lat,lon)

    def add(self):
        cur = conn.execute('insert into journey (b_id,board,date,start,end,gps) values(?,?,?,?,?,?),',
                           (self.b_id, self.board, self.date, self.start, self.end, self.gps))
        conn.commit()
        return cur.lastrowid

    @staticmethod
    def active_ride(for_date):
        cur = conn.execute('select * from journey where date=?', (for_date))
        if cur.rowcount == 0:
            return False
        else:
            return cur.fetchall()

    ''' transaction to perform following operation
    1) create a new a journey record
    2) update driver.active-journey-b-id by last inserted row id
    '''

    @staticmethod
    def trans_create_journey(journey_type, date, bus_id, user_id):
        cur = conn.cursor()
        # begin transaction
        cur.execute('begin')
        cur.execute('insert into journey (j_type,date,start,b_id) values (?,?,?,?)', (journey_type, date, date, bus_id))
        cur.execute('update driver set active_ride_j_id=last_insert_rowid() where userid=?', [user_id])
        cur.execute('commit')

    # update new gps location
    @staticmethod
    def update_gps(journey_id, gps):
        cur = conn.execute('update journey set gps=?,last_update=? where id=?',
                           (gps, utils.get_date_full(), journey_id))
        conn.commit()



