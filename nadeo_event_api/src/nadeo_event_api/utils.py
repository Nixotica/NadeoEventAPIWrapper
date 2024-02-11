from datetime import datetime

import pytz


def dt_standardize(date: datetime):
    if date.tzinfo is not None:
        date = date.astimezone(pytz.utc)
    return date.replace(tzinfo=None)