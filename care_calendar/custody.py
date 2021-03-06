"""Calculates custody."""

import calendar
from datetime import date, datetime, timedelta
from typing import List

from .utils import week_id


EASTER_SUNDAY = {
    2021: date(2021, 4, 4),
    2022: date(2022, 4, 17),
    2023: date(2023, 4, 9),
    2024: date(2024, 3, 31),
    2025: date(2025, 4, 20),
    2026: date(2026, 4, 5),
    2027: date(2027, 3, 28),
    2028: date(2028, 4, 16),
    2029: date(2029, 4, 1),
    2030: date(2030, 4, 21),
    2031: date(2031, 4, 13),
    2032: date(2032, 3, 28),
    2033: date(2033, 4, 17),
    2034: date(2034, 4, 9),
    2035: date(2035, 3, 25),
    2036: date(2036, 4, 13),
    2037: date(2037, 4, 5),
    2038: date(2038, 4, 25),
    2039: date(2039, 4, 10),
    2040: date(2040, 4, 1),
}

PENTECOST = {year: day + timedelta(49) for year, day in EASTER_SUNDAY.items()}


def get_all_sunday(month: int, year: int) -> List[date]:
    """Returns all Sundays for a given month and year."""
    cal = calendar.Calendar()
    return [
        d
        for d in cal.itermonthdates(year, month)
        if d.month == month and day_is_sunday(d)
    ]


def get_mother_day(year: int) -> date:
    """Returns the day of Mother's day.

    Mother's day is the last Sunday of May unless it is the Pentecost.
    """
    sundays = get_all_sunday(5, year)
    if sundays[-1] == PENTECOST[year]:
        return sundays[-1] + timedelta(7)
    return sundays[-1]


def get_father_day(year: int) -> date:
    """Returns the day of Father's day.

    Father's day is the 3rd Sunday of June.
    """
    return get_all_sunday(6, year)[2]


def is_mother_day(day: date) -> bool:
    """Returns True if a day is Mother's day."""
    return day == get_mother_day(day.year)


def is_father_day(day: date) -> bool:
    """Returns True if a day is father's day (3rd Sunday of June)."""
    return day == get_father_day(day.year)


def is_even_year(day: date) -> bool:
    """Returns True is a year is even."""
    return day.year % 2 == 0


def is_even_week(day: date) -> bool:
    """Returns True is a week is even."""
    return week_id(day) % 2 == 0


def is_odd_week(day: date) -> bool:
    """Returns True is a week is odd."""
    return not is_even_week(day)


def day_is_monday(day: date) -> bool:
    return day.weekday() == 0


def day_is_tuesday(day: date) -> bool:
    return day.weekday() == 1


def day_is_wednesday(day: date) -> bool:
    return day.weekday() == 2


def day_is_thursday(day: date) -> bool:
    return day.weekday() == 3


def day_is_friday(day: date) -> bool:
    return day.weekday() == 4


def day_is_saturday(day: date) -> bool:
    return day.weekday() == 5


def day_is_sunday(day: date) -> bool:
    return day.weekday() == 6


def day_is_weekend(day: date) -> bool:
    return day.weekday() > 4


def next_day(day: date) -> date:
    """Returns the next day."""
    return day + timedelta(1)


def previous_day(day: date) -> date:
    """Returns the previous day."""
    return day - timedelta(1)


def day_is_holiday(day: date, holiday_list: List[List[date]]) -> bool:
    """Returns True if a date is in the list of holidays."""
    for holiday in holiday_list:
        if day in holiday:
            return True
    return False


def next_day_is_holiday(day: date, holiday_list: List[List[date]]) -> bool:
    """Returns True if the day after a date is in the list of holidays."""
    return day_is_holiday(next_day(day), holiday_list)


def previous_day_is_holiday(day: date, holiday_list: List[List[date]]) -> bool:
    """Returns True if the day before a date is in the list of holidays."""
    return day_is_holiday(previous_day(day), holiday_list)


def get_holidays(day: date, holiday_list: List[List[date]]) -> List[date]:
    """Returns the holidays a date belongs to."""
    for holiday in holiday_list:
        if day in holiday:
            return holiday
    return []


def half_holiday(holidays: List[date]) -> date:
    """Returns the date that corresponds to half the holidays."""
    delta = timedelta(len(holidays) / 2)
    return holidays[0] + delta


def guardian_transition(first: str, second: str) -> str:
    """Returns a string corresponding to a transition from first to second guardian."""
    return f"{first}???{second}"


def is_last_day_of_holidays(day: date, holidays: List[date]) -> bool:
    """Returns True if a day is the last day of holidays."""
    return day == holidays[-1]


def get_guardian_even_week(day: date, holiday_list: List[List[date]]) -> str:
    """Get the guardian for a day, on even weeks."""
    if next_day_is_holiday(day, holiday_list):
        guardian = get_guardian_holidays(next_day(day), holiday_list)
        if guardian == "L":
            return "L"
        return guardian_transition("L", "B")
    if day_is_tuesday(day):
        return guardian_transition("L", "B")
    if day_is_wednesday(day):
        return guardian_transition("B", "L")
    if day_is_friday(day):
        return guardian_transition("L", "B")
    if day_is_weekend(day):
        return "B"
    return "L"


def get_guardian_odd_week(day: date, holiday_list: List[List[date]]) -> str:
    """Get the guardian for a day, on even weeks."""
    if next_day_is_holiday(day, holiday_list):
        guardian = get_guardian_holidays(next_day(day), holiday_list)
        if guardian == "B":
            return "B"
        return guardian_transition("B", "L")
    if day_is_friday(day):
        return guardian_transition("B", "L")
    if day_is_weekend(day):
        return "L"
    return "B"


def get_guardian_holidays(day: date, holiday_list: List[List[date]]) -> str:
    """Returns the guardian on an holiday day."""
    holidays = get_holidays(day, holiday_list)
    day_before_half = previous_day(half_holiday(holidays))
    if is_even_year(day):
        first, second = "L", "B"
    else:
        first, second = "B", "L"
    if day == day_before_half:
        return guardian_transition(first, second)
    if day < day_before_half:
        return first
    # Now we're in the second half.
    # If is January, the guardian is the second guardian from last year.
    if day.month == 1:
        first, second = second, first
    if is_last_day_of_holidays(day, holidays):
        guardian = get_guardian_regular_week(next_day(day), holiday_list)
        if guardian[0] != second:
            return guardian_transition(second, first)
    return second


def get_guardian_regular_week(day: date, holiday_list: List[List[date]]) -> str:
    """Returns the guardian on a regular week i.e. not holidays."""
    if is_even_week(day):
        return get_guardian_even_week(day, holiday_list)
    if is_odd_week(day):
        return get_guardian_odd_week(day, holiday_list)


def get_guardian(day: date, holiday_list: List[List[date]]) -> str:
    """Get the guardian for a day, according to the holidays."""
    if is_father_day(day):
        return "B"
    if is_mother_day(day):
        return "L"
    if day_is_holiday(day, holiday_list):
        return get_guardian_holidays(day, holiday_list)
    return get_guardian_regular_week(day, holiday_list)
