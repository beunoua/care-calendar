"""care.calendar day status.

Status is essentially a day that will have a specific css
so that it will be displayed in a specific fashion.
"""

import datetime

def str_to_date(date_string: str, year: int = None) -> datetime.date:
    """Returns a `datetime.date` from a string."""
    tokens = date_string.split("/")
    if len(tokens) == 2:
        day, month = tokens
    elif len(tokens) == 3:
        day, month, year = tokens
        if len(year) == 2:
            year = "20{}".format(year)
    else:
        raise ValueError("Invalid date string: '{}'".format(date_string))
    try:
        return datetime.date(int(year), int(month), int(day))
    except ValueError as exc:
        raise ValueError(f"day is out of range: {year}/{month}/{day}") from exc

