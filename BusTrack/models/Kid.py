from BusTrack import db, conn


class Kid():
    __TABLE__ = 'kid'

    def __init__(self, name=None, section=None, photo=None, parent_id=None, bus_id=None, id=None):
        self.id = id
        self.name = name
        self.section = section
        self.photo = photo
        self.p_id = parent_id  # parent id
        self.b_id = bus_id

    def get_all(self):
        cur = conn.execute('select * from kid')
        return cur.fetchall()

    def add_if_not_exist(self):
        cur = conn.execute('select * from kid')

    def add(self):
        try:
            cur = conn.execute('insert into kid (name,section,photo,p_id,b_id) values(?,?,?,?,?)',
                               (self.name, self.section, self.photo, self.p_id, self.b_id))
            conn.commit()
        except:
            return None
        return cur.lastrowid

    # get kids of particular parent
    @staticmethod
    def get_kids(parent_id):
        cur = conn.execute('select * from kid where p_id=?', (parent_id))
        return cur.fetchall()

    # ---------------------code used in driver module-----------------------#
    # here j_id is known
    # get kids who whose attendance is not yet taken for this bus journey
    @staticmethod
    def get_kid_ids(journey_id):
        cur = conn.execute('select kid.id from kid where kid.id not in( \
            select kid.id from attendance inner join kid on attendance.k_id=kid.id \
            where j_id=?) and  kid.b_id=(select journey.b_id from journey where journey.id=?)',
                           [journey_id, journey_id])
        return Kid.id_to_list(cur.fetchall())

    # get kid ids whose dropped present is not yet taken
    @staticmethod
    def get_kid_drop_not_present(journey_id):
        cur = conn.execute('select attendance.k_id from attendance where j_id=? and pick_present=1 \
            and drop_present=0 ', [journey_id])
        return Kid.id_to_list(cur.fetchall())

    @staticmethod
    def id_to_list(cur):
        if cur is None:
            return []
        else:
            return [i[0] for i in cur]

    # get image link of this kid ,only those image for which this driver is authorized
    @staticmethod
    def get_image_for_driver(token, kid_id):
        cur = conn.execute('select kid.photo from kid where kid.b_id=(select driver.b_id from driver where token=? \
                         ) and kid.id=?', [token, kid_id])
        r = cur.fetchone()
        if r is None:
            return r
        else:
            return r[0]

    # get image link of this kid ,only those image for which this parent is authorized
    @staticmethod
    def get_image_for_parent(token,kid_id):
        cur=conn.execute('select kid.photo from kid inner join parent on kid.p_id=parent.id  \
            where parent.token=? and kid.id=? ',[token,kid_id])
        r = cur.fetchone()
        if r is None:
            return r
        else:
            return r[0]

            # ---------------------driver module ends------------------------#
            # -------------------- code for parent module--------------------#

