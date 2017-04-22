from BusTrack import db, conn
from BusTrack.helpers import dbHelpers
from BusTrack.helpers import utils


# code for 'driver' table
class Driver():
    def __init__(self, user_id=None, name=None, contact=None, password=None, bus_id=None):
        self.name = name
        self.contact = contact
        self.password = password
        self.b_id = bus_id
        self.userid = user_id

    def add(self):
        cur = conn.execute('insert into driver (name,contact,password,b_id,userid) values (?,?,?,?,?)'
                           , [self.name, self.contact, self.password, self.b_id, self.userid])
        print([self.name, self.contact, self.password, self.b_id, self.userid])
        conn.commit()
        return cur.lastrowid

    def get_all(self):
        cur = conn.execute('select * from driver')
        return cur.fetchall()

    @staticmethod
    def get_user(userid):  # check password
        cur = conn.execute(
            'select driver.name,driver.password,bus.b_no,driver.active_ride_j_id, bus.id from driver inner join Bus '
            'on driver.b_id=bus.id where driver.userid=? ', [userid])
        user = cur.fetchone()
        if user is None:
            return False
        else:
            return user  # {1:"pass","3":"active ride","4":"bus_id"}

    @staticmethod
    def update_token(token, expires, userid):
        cur = conn.execute('update driver set token=?,expires=? where userid=?', [token, expires, userid])
        conn.commit()

    @staticmethod
    def is_unique(user_id):
        # method used in Validation unique entity
        # check weather given 'user_id' already exist in Driver table
        cur = conn.execute('select * from driver where userid=? ', [user_id])  # pass sequence
        return dbHelpers.row_zero(cur)

    @staticmethod
    def get_all_allocated():
        # registered driver who are assigned a bus
        cur = conn.execute('select userid,name, b_no,contact  from bus_driver')
        return cur.fetchall()

    # check if this token is allocated to any driver and is still valid
    @staticmethod
    def is_valid_token(token):
        date = utils.get_date_full()
        cur = conn.execute('select userid from driver where token=? and DATETIME(expires) > DATETIME(?)', (token, date))
        user = cur.fetchone()
        if user is None:
            return False
        else:
            return True

    # get current active ride detail ,else return None
    @staticmethod
    def get_active_ride(token):
        cur = conn.execute('select active_ride_j_id from driver where token=?', [token])
        j_id = cur.fetchone()
        if j_id is None:
            return None
        else:
            return j_id[0]

    # check if driver has already completed @j_type ride for @date
    @staticmethod
    def is_ride_already_completed(userid, j_type, date=utils.get_date_only()):
        cur = conn.execute('select * from journey inner join bus on bus.id=journey.b_id inner join driver'
                           ' on driver.b_id=bus.id where driver.userid=? '
                           ' and date(journey.date)=date(?) and journey.j_type=? and journey.end is not 0 ', [userid, date, j_type])
        res = cur.fetchone()
        if res is None:
            return False  # no ride yet
        else:
            return True

    @staticmethod
    def logout_session(token):
        # set end journey time
        # set token,expiry and active_b_id to null
        cur = conn.cursor()
        cur.execute('begin')
        cur.execute('update journey set end=? where id=(select active_ride_j_id  from driver where token=?)',
                    (utils.get_date_full(), token))
        cur.execute("update driver set active_ride_j_id=?,token=?,expires=? WHERE token=?", ('', '', '', token))
        cur.execute('commit')
