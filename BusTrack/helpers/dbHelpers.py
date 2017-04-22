# common database helper function
def row_zero(cursor):
    l=cursor.fetchone()
    if l is None:
        return True # length 0
    else:
        return False

