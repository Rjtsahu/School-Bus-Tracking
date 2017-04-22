from BusTrack import conn
from BusTrack.helpers import utils


class Parent():
    __TABLE__ = 'parent'

    def __init__(self, name=None, password=None, email=None, phone=None, home_gps=None):
        self.name = name
        self.password = password
        self.email = email
        self.phone = phone
        self.home_gps = home_gps

    def get_all(self):
        cur = conn.execute('select * from parent')
        return cur.fetchall()

    def add(self):
        cur = conn.execute('insert into parent (name,password,email,phone,home_gps) values(?,?,?,?,?)',
                           (self.name, self.password, self.email, self.phone, self.home_gps))
        conn.commit()
        return cur.lastrowid

    def add_or_get(self):
        # refer link:admin.kid
        cur = conn.execute('select id from parent where email=? ', [self.email])
        res = cur.fetchone()
        print(res)
        if res is None:
            # create new record
            res = self.add()
            return res
        else:
            return res[0]

    # get user having email =?
    @staticmethod
    def get_user(email):
        cur = conn.execute('select * from parent where email=?', [email])
        if cur.rowcount == 0:
            return False
        else:
            return cur.fetchone()

    @staticmethod
    def get_all_parent_with_kid():
        # get data from parent_kid view
        cur = conn.execute('select * from parent_kid')
        print(cur.description)
        return cur.fetchall()

    @staticmethod
    def get_all_parent_kid_with_bus():
        # get data from parent_kid_bus view
        cur = conn.execute('select * from parent_kid_bus')
        print(cur.description)
        return cur.fetchall()

    # -------------- code used in Parent Module--------------#

    # get parent from token
    @staticmethod
    def get_parent_id(token):
        cur = conn.execute('select * from parent where token=? ', [token])
        return cur.fetchone()

    @staticmethod
    def update_token(email, token, expire):
        cur = conn.execute('update parent set token=?,expires=? where email=?',
                           [token, expire, email])
        conn.commit()

        # check if this token is allocated to any driver and is still valid

    @staticmethod
    def is_valid_token(token):
        date = utils.get_date_full()
        cur = conn.execute('select email from parent where token=? and DATETIME(expires) > DATETIME(?)', (token, date))
        user = cur.fetchone()
        if user is None:
            return False
        else:
            return True

    # check weather @param#k_id belongs to parent having token @param#token
    @staticmethod
    def is_kidOf(kid_id, token):
        cur = conn.execute('select kid.id from kid inner join parent on kid.p_id=parent.id '
                           'where kid.id=? and parent.token=? ', [kid_id, token])
        res = cur.fetchone()
        if res is None:
            return False
        else:
            return True

    @staticmethod
    def get_kids(token):
        cur = conn.execute('select kid.id,name,section,photo,bus.id,bus.b_no from kid inner join bus on kid.b_id=bus.id where kid.p_id = \
            (select parent.id from parent where parent.token=? )', [token])
        return Parent.kids_to_obj_list(cur.fetchall())

    @staticmethod
    def kids_to_obj_list(cur):
        if cur is None:
            return None
        l = []
        for c in cur:
            k = {"id": c[0], "name": c[1], "section": c[2], "photo": c[3]}
            b = {"bus_id": c[4], "bus_name": c[5]}
            k_b = {"kid": k, "bus": b}
            l.append(k_b)
        return l
