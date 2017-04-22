import random
# some frequent utility function
def rand(length=20):
    chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
    str_len=len(chars)
    str=""
    for i in range(length):
        index=random.randint(0,str_len-1)
        str+=chars[index]
    return str


# get date
# later research about how to store date time in sqlite
def get_date_full():
    import datetime
    d=str(datetime.datetime.today())
    d=d[0:19]
    return d

# generate expiry date used to validate token
EXPIRY_IN_DAY=3
def get_expiry_date_full():
    import datetime
    d= datetime.datetime.now()+datetime.timedelta(days=EXPIRY_IN_DAY)
    return str(d)[:19]