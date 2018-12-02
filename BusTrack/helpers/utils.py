import random
import string


# some frequent utility function
def rand(length=20):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


# get date
# later research about how to store date time in sqlite
def get_date_full():
    d = get_local_time()
    d = d[0:19]
    return d


# get date only
def get_date_only():
    d = get_local_time()
    d = d[0:10]
    return d


# get current time
def get_time_only():
    t = get_local_time()
    t = t[11:19]
    return t


# generate expiry date used to validate token
EXPIRY_IN_DAY = 3


def get_expiry_date_full():
    import datetime
    from pytz import timezone
    d = datetime.datetime.now(timezone('Asia/Kolkata')) + datetime.timedelta(days=EXPIRY_IN_DAY)
    return str(d)[:19]


TIME_DELTA = 1  # 1 minute


# use to add location when last_update_time<current_time-delta
# return current time - delta time
def get_prev_time():
    import datetime
    from pytz import timezone
    d = datetime.datetime.now(timezone('Asia/Kolkata')) - datetime.timedelta(minutes=TIME_DELTA)
    return str(d)[:19]


def get_local_time(zone='Asia/Kolkata'):
    import datetime
    from pytz import timezone
    other_zone = timezone(zone)
    other_zone_time = datetime.datetime.now(other_zone)
    return str(other_zone_time)


def get_loc(txt):
    from geopy.geocoders import Nominatim
    from pprint import pprint
    a = Nominatim()

    res = a.geocode(query=txt, exactly_one=False, timeout=10000)
    pprint(res)
