"""kaloot.custody - Provides functions to get the guardian for a given day."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .date import date, date_collection
from .event import Event, parse_date_list

GUARDIANS = ("B", "L")


@dataclass
class CustomCare:
    """Days on which the guardian is agreed upon instead of computed from the rules.

    Each period is a ``date_collection`` associated with the guardian for those days.
    """

    event: Event
    periods: list[tuple[date_collection, str]] = field(default_factory=list)

    @classmethod
    def from_yaml(
        cls, name: str, data: dict[str, Any], year: int
    ) -> CustomCare:
        """Creates a ``CustomCare`` from YAML data.

        Expected format::

            css_class: "customcare"
            dates:
              - dates: 20/12/2025 - 04/01/2026
                care: B
        """
        for key in ("css_class", "dates"):
            if key not in data:
                raise KeyError(f"Misformatted '{name}': missing required field '{key}'")

        all_dates = date_collection()
        periods = []
        for item in data["dates"]:
            if not isinstance(item, dict) or "dates" not in item or "care" not in item:
                raise ValueError(
                    f"{name}: each entry must have 'dates' and 'care' fields, got {item!r}"
                )
            if item["care"] not in GUARDIANS:
                raise ValueError(
                    f"{name}: invalid 'care' value {item['care']!r}, "
                    f"expected one of {GUARDIANS}"
                )
            dates = parse_date_list(name, [item["dates"]], year)
            all_dates.ranges.extend(dates.ranges)
            all_dates.date_list.extend(dates.date_list)
            periods.append((dates, item["care"]))

        return cls(Event(name, data["css_class"], all_dates), periods)

    def guardian(self, day: date) -> str | None:
        """Returns the agreed guardian for a day, or ``None`` if the day is not custom."""
        for dates, guardian in self.periods:
            if day in dates:
                return guardian
        return None


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
        return holidays.half().previous()
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


def get_guardian_with_custom(
    day: date, holidays: date_collection, custom: CustomCare | None
) -> str:
    """Get the guardian for a day, taking custom care agreements into account.

    Transitions are shown on the last day before a custom period, and on the last
    day of a custom period, when the guardian changes.
    """
    if custom is None:
        return get_guardian(day, holidays)

    next_day = day.next()
    next_custom = custom.guardian(next_day)

    guardian = custom.guardian(day)
    if guardian is not None:
        if next_custom is None:
            next_guardian = get_guardian(next_day, holidays)[0]
            if next_guardian != guardian:
                return guardian_transition(guardian, next_guardian)
        elif next_custom != guardian:
            return guardian_transition(guardian, next_custom)
        return guardian

    guardian = get_guardian(day, holidays)
    if next_custom is None or guardian[-1] == next_custom:
        return guardian
    if guardian[0] == next_custom:
        return next_custom
    return guardian_transition(guardian[0], next_custom)


def is_summer_holidays(holidays: date_collection) -> bool:
    """Returns True if the holidays are summer holidays."""
    return 6 <= holidays[0].month <= 7


def is_regular_holidays(holidays: date_collection) -> bool:
    """Returns True if the holidays are regular holidays, i.e. not summer holidays."""
    return not is_summer_holidays(holidays)
