# handle feedback given by user
from BusTrack import conn


class Feedback():
    __TABLE__ = 'feedback'

    def __init__(self, name=None, email=None, title=None, message=None, date=None, p_id=None, d_id=None):
        self.name = name
        self.email = email
        self.title = title
        self.message = message
        self.date = date
        self.parent_id = p_id  # NOT MUST: provides better functionality if available
        self.driver_id = d_id  # NOT MUST: provides better functionality if available

    def get_all(self):
        cur = conn.execute('select id,name,email,title,message, date(date) as date, time(date) as time from feedback order by id desc limit 40')
        return cur.fetchall()

    def add(self):
        cur = conn.execute('insert into feedback (name,email,title,message,date,p_id,d_id) values (?,?,?,?,?,?,?)',
                           (self.name, self.email, self.title, self.message, self.date, self.parent_id, self.driver_id))
        conn.commit()
        return cur.lastrowid
