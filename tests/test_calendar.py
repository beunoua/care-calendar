from kaloot.calendar import Calendar

from calendar import monthrange, monthcalendar
import datetime
from typing import Callable

from hypothesis import given
from hypothesis.strategies import composite, integers, SearchStrategy


@composite
def calendar(draw: Callable[SearchStrategy[int], int]) -> Calendar:
    # calendar.monthdatescalendar() pads the last week of December with dates from
    # the following year, which overflows for datetime.MAXYEAR.
    random_year = draw(
        integers(min_value=datetime.MINYEAR, max_value=datetime.MAXYEAR - 1)
    )
    return Calendar(random_year)


def number_of_days_in_month(year: int, month: int) -> int:
    return monthrange(year, month)[1]


def number_of_weeks_in_month(year: int, month: int) -> int:
    return len(monthcalendar(year, month))


@given(calendar(), integers(min_value=1, max_value=12))
def test_iter_month_dates(cal: Calendar, month_id: int):
    dates = list(cal.iter_month_dates(month_id))
    expected = len(dates)
    assert expected == number_of_days_in_month(cal.year, month_id)
    for date in dates:
        assert date.year == cal.year
        assert date.month == month_id


@given(calendar(), integers(min_value=1, max_value=12))
def test_iter_month_weeks(cal: Calendar, month_id: int):
    weeks = list(cal.iter_month_weeks(month_id))
    expected = len(weeks)
    assert expected == number_of_weeks_in_month(cal.year, month_id)
    assert sum(len(week) for week in weeks) == number_of_days_in_month(cal.year, month_id)
    for week in weeks:
        for date in week:
            assert date.year == cal.year
            assert date.month == month_id


if __name__ == "__main__":
    test_iter_month_dates()
