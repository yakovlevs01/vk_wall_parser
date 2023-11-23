import datetime


def convert_unixtime_to_datetime(unixtime):
    return datetime.datetime.fromtimestamp(unixtime).strftime("%d.%m.%Y, %H:%M:%S")


def is_sunday(unixtime):
    dt = datetime.datetime.utcfromtimestamp(unixtime)
    return dt.weekday() == 6


def is_after(unixtime, some_datetime_unix):
    return int(unixtime) > int(some_datetime_unix)


date_stop = 1474146000  # 18 сентября 2016 0:00
