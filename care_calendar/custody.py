"""Calculates custody."""

from datetime import date, datetime, timedelta
from typing import List

from .utils import week_id


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
    return f"{first}→{second}"


def get_guardian_even_week(day: date, holiday_list: List[List[date]]) -> str:
    """Get the guardian for a day, on even weeks."""
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
    if day_is_friday(day):
        if next_day_is_holiday(day, holiday_list):
            guardian = get_guardian_holidays(next_day(day), holiday_list)
            if guardian == "B":
                return "B"
        return guardian_transition("B", "L")
    if day_is_weekend(day):
        return "L"
    return "B"


def is_last_day_of_holidays(day: date, holidays: List[date]) -> bool:
    """Returns True if a day is the last day of holidays."""
    return day == holidays[-1]


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
    if is_last_day_of_holidays(day, holidays):
        guardian = get_guardian_regular_week(next_day(day), holiday_list)
        if guardian != second:
            return guardian_transition(second, guardian)
    return second


def get_guardian_regular_week(day: date, holiday_list: List[List[date]]) -> str:
    """Returns the guardian on a regular week i.e. not holidays."""
    if is_even_week(day):
        return get_guardian_even_week(day, holiday_list)
    if is_odd_week(day):
        return get_guardian_odd_week(day, holiday_list)


def get_guardian(day: date, holiday_list: List[List[date]]) -> str:
    """Get the guardian for a day, according to the holidays."""
    if day_is_holiday(day, holiday_list):
        return get_guardian_holidays(day, holiday_list)
    return get_guardian_regular_week(day, holiday_list)
