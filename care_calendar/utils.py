"""care_calendar miscelleanous functions"""

import datetime


def current_year() -> int:
    return datetime.datetime.now().year

def week_id(day: datetime.date) -> int:
    """Returns a day week number."""
    return day.isocalendar()[1]
