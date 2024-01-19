from datetime import datetime


def dt_standardize(date: datetime):
    return date.replace(tzinfo=None)