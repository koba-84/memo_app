# utils.py
from datetime import timezone, timedelta

JST = timezone(timedelta(hours=9))


def to_jst(dt):
    if dt is None:
        raise ValueError("Input datetime cannot be None")
    try:
        return dt.replace(tzinfo=timezone.utc).astimezone(JST)
    except Exception:
        raise ValueError("Invalid datetime format")
