from .. import db,conn
# code for 'bus' table

class Bus():
    def __init__(self, bus_no=None, bus_detail=None):
        self.b_no=bus_no
        self.detail=bus_detail


    def get_all(self):
        qry='select * from bus'
        cur=conn.execute(qry)
        return cur.fetchall()

    def add(self):
        cur=conn.execute('insert into bus (b_no,detail) values(?,?)',(self.b_no,self.detail))
        conn.commit()
        return cur.lastrowid

    @staticmethod
    def is_unique(bus_id):
        # method used in Validation unique entity
        # check weather given bus already allocated to  Driver table
        cur = conn.execute('select * from bus_driver where id=?', (bus_id))
        return cur.rowcount == 0

    @staticmethod
    def unallocated_bus():
        # return buses that are currently unallocated
        cur=conn.execute('select id,b_no from bus where id not in (select id from bus_driver)')
        return cur.fetchall()
