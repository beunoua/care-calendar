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


def get_holidays_transition_date(holidays: date_collection) -> date:
    """Returns the transition date for a given set of holidays.

    On regular holidays, the transition day is always the first Saturday of the holidays.

    On summer holidays, the transition is the day in the middle of the holidays.
    If the number of holiday days is odd, the August guardian gets one more day than
    the July guardian, so the transition is the day before the half.
    """
    if is_summer_holidays(holidays):
        if holidays.has_odd_number_of_days():
            return holidays.half().previous()
        return holidays.half()
    return holidays[0].next_saturday()


def get_guardian_holidays(day: date, holidays: date_collection) -> str:
    """Returns the guardian on an holiday day."""

    first, second = "B", "L"
    if day.is_even_year():
        first, second = "L", "B"

    holidays = get_holidays(day, holidays)
    transition_day = get_holidays_transition_date(holidays)

    if day < transition_day:
        return first

    if day == transition_day:
        return guardian_transition(first, second)

    # Now we're in the second half.
    # If it is January, the guardian is the second guardian from last year.
    if day.month == 1:
        first, second = second, first

    # If it is the last day of the holidays, we need to check the next day:
    # if the guardian on the next day is not the current guardian, we need to transition.
    if day.is_last_day_of(holidays):
        guardian = get_next_week_guardian(day, holidays)
        if guardian[0] != second:
            return guardian_transition(second, first)
    return second


def get_next_week_guardian(day: date, holidays: date_collection) -> str:
    """Returns the guardian for the next week."""
    return get_guardian_regular_week(day.next(), holidays)


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


def is_summer_holidays(holidays: date_collection) -> bool:
    """Returns True if the holidays are summer holidays."""
    return 6 <= holidays[0].month <= 7


def is_regular_holidays(holidays: date_collection) -> bool:
    """Returns True if the holidays are regular holidays, i.e. not summer holidays."""
    return not is_summer_holidays(holidays)
