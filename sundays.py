import datetime


def convert_unixtime_to_datetime(unixtime):
    return datetime.datetime.fromtimestamp(unixtime).strftime("%d.%m.%Y, %H:%M:%S")


def is_sunday(unixtime):
    dt = datetime.datetime.utcfromtimestamp(unixtime)
    return dt.weekday() == 6


def is_after(unixtime, some_datetime_unix):
    return int(unixtime) > int(some_datetime_unix)


date_stop = 1474146000  # 18 сентября 2016 0:00




def get_all_weekly_dates(start, stop) -> list[int]:
    res = []
    while start > stop:
        res.append(start)
        start -= ONEDAY * 7
    return res


def time_is_in_unterval(time, t_start, t_finish) -> bool:
    return time >= t_start and time <= t_finish


def is_appropriate_post(post_unixtime, list_of_dates):
    return any(
        [
            time_is_in_unterval(post_unixtime, x - ONEDAY // 2, x + ONEDAY // 2)
            for x in list_of_dates
        ]
    )


ONEDAY = 24 * 60 * 60
midday = 1695546000  # Пример: 24 сентября 2023 12:00:00
sundays_to_2016 = get_all_weekly_dates(midday, 1474146000 - ONEDAY)

str_sundays_to_2016 = [
    convert_unixtime_to_datetime(x)
    for x in get_all_weekly_dates(midday, 1474146000 - ONEDAY)
]
