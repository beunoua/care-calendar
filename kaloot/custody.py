"""kaloot.custody - Provides functions to get the guardian for a given day."""

from .date import date, date_collection


def guardian_transition(first: str, second: str) -> str:
    """Returns a string corresponding to a transition from first to second guardian."""
    return f"{first}→{second}"


def get_holidays(day: date, holidays: date_collection) -> date_collection:
    """Returns the holidays a date belongs to."""
    for range_ in holidays.ranges:
        if day in range_:
            return range_.ascollection()
    return date_collection([])


def get_guardian_holidays(day: date, holidays: date_collection) -> str:
    """Returns the guardian on an holiday day."""

    first, second = "B", "L"
    if day.is_even_year():
        first, second = "L", "B"

    holidays = get_holidays(day, holidays)
    day_before_half = holidays.half().previous()

    if day == day_before_half:
        return guardian_transition(first, second)

    if day < day_before_half:
        return first

    # Now we're in the second half.
    # If it is January, the guardian is the second guardian from last year.
    if day.month == 1:
        first, second = second, first

    if day == holidays[-1]:
        guardian = get_guardian_regular_week(day.next(), holidays)
        if guardian[0] != second:
            return guardian_transition(second, first)
    return second


def get_guardian_even_week(day: date, holidays: date_collection) -> str:
    """Get the guardian for a day, on even weeks."""
    if day.next() in holidays:
        guardian = get_guardian_holidays(day.next(), holidays)
        if guardian == "L":
            return "L"
        return guardian_transition("L", "B")
    if day.is_tuesday():
        return guardian_transition("L", "B")
    if day.is_wednesday():
        return guardian_transition("B", "L")
    if day.is_friday():
        return guardian_transition("L", "B")
    if day.is_weekend():
        return "B"
    return "L"


def get_guardian_odd_week(day: date, holidays: date_collection) -> str:
    """Get the guardian for a day, on even weeks."""
    if day.next() in holidays:
        guardian = get_guardian_holidays(day.next(), holidays)
        if guardian == "B":
            return "B"
        return guardian_transition("B", "L")
    if day.is_friday():
        return guardian_transition("B", "L")
    if day.is_weekend():
        return "L"
    return "B"


def get_guardian_regular_week(day: date, holidays: date_collection) -> str:
    """Returns the guardian on a regular week i.e. not holidays."""
    if day.is_even_week():
        return get_guardian_even_week(day, holidays)
    if day.is_odd_week():
        return get_guardian_odd_week(day, holidays)
    raise RuntimeError(f"{day}: week appears to be neither even or odd")


def get_guardian(day: date, holidays: date_collection) -> str:
    """Get the guardian for a day."""
    if day.is_fathers_day():
        return "B"
    if day.is_mothers_day():
        return "L"
    if day in holidays:
        return get_guardian_holidays(day, holidays)
    return get_guardian_regular_week(day, holidays)
