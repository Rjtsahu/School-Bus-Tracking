# represent a gps tuple which can be stored in single field in table
# as latitude,longitude
import numbers

DELIMITER = ','


class Gps:
    @staticmethod
    def get_from_str(gps_tuple_str):
        lat = 0
        lon = 0
        if gps_tuple_str is not None:
            try:
                (lat, lon) = gps_tuple_str.split(DELIMITER)
                lat = float(lat)
                lon = float(lon)
                if not isinstance(lat, float):
                    lat = 0
                elif not isinstance(lon, float):
                    lon = 0
                print(lat, lon)
            except:
                print('cant split to lat long')
                return (0, 0)
        return (lat, lon)

    @staticmethod
    def tuple_to_str(lat, lon):
        try:
            lat = float(lat)
            lon = float(lon)
            return '%s,%s' % (lat, lon)
        except:
            print('incorrect gps input')
            return '0,0'
