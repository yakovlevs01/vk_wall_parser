import datetime


def convert_unixtime_to_datetime(unixtime: int) -> str:
    return datetime.datetime.fromtimestamp(
        unixtime,
        tz=datetime.tzinfo.utcoffset(3),
    ).strftime(
        "%d.%m.%Y, %H:%M:%S",
    )


def is_sunday(unixtime: int) -> bool:
    sunday = 6
    dt = datetime.datetime.fromtimestamp(unixtime, tz=datetime.tzinfo.utcoffset(3))
    return dt.weekday() == sunday


def is_after(unixtimestamp: int, other_unixtimestamp: int) -> bool:
    return int(unixtimestamp) > int(other_unixtimestamp)
