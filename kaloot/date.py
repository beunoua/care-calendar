"""Provides the ``date``, ``date_range`` and ``date_collection`` classes."""

from __future__ import annotations

import collections
from dataclasses import dataclass, field
import datetime
from typing import Iterator, Optional


def current_year() -> int:
    """Returns the current year."""
    return datetime.datetime.now().year


class date(datetime.date):  # pylint: disable=invalid-name  # conforms to datetime.date
    """Provides a date class with additional methods compared to ``datetime.date``.

    The ``date`` class also provides a ``description`` attribute that can be used to
    store a description of the date.
    """

    description: str

    def __new__(cls, *args, **kwargs):
        description = kwargs.pop("description", "")
        obj = super().__new__(cls, *args, **kwargs)
        obj.description = description
        return obj

    def name(self) -> str:
        """Returns the name of the date's day."""
        return self.strftime("%A")

    @classmethod
    def from_string(cls, date_string: str, year: int = current_year()) -> date:
        """Returns a new `date` from a string."""
        tokens = [token.strip() for token in date_string.split("/")]
        if len(tokens) == 3:
            day_s, month_s, year_s = tokens
            if len(year_s) == 2:
                year_s = f"20{year_s}"
            day, month, year = int(day_s), int(month_s), int(year_s)
        elif len(tokens) == 2:
            day_s, month_s = tokens
            day, month = int(day_s), int(month_s)
        else:
            raise ValueError(f"Invalid date string: {date_string:!r}")
        try:
            return cls(year, month, day)
        except ValueError as exc:
            raise ValueError(f"day is out of range: {year}/{month}/{day}") from exc

    @classmethod
    def from_date(cls, day: datetime.date) -> date:
        """Returns a new ``date`` from a ``datetime.date``."""
        return cls.fromordinal(day.toordinal())

    def astuple(self) -> tuple[int, int, int]:
        """Returns a tuple of the date's year, month and day."""
        return (self.year, self.month, self.day)

    def weekid(self) -> int:
        """Returns the week number of the year."""
        return self.isocalendar()[1]

    def is_monday(self):
        """Returns ``True`` if the date is a Monday, ``False`` otherwise."""
        return self.weekday() == 0

    def is_tuesday(self):
        """Returns ``True`` if the date is a Tuesday, ``False`` otherwise."""
        return self.weekday() == 1

    def is_wednesday(self):
        """Returns ``True`` if the date is a Wednesday, ``False`` otherwise."""
        return self.weekday() == 2

    def is_thursday(self):
        """Returns ``True`` if the date is a Thursday, ``False`` otherwise."""
        return self.weekday() == 3

    def is_friday(self):
        """Returns ``True`` if the date is a Friday, ``False`` otherwise."""
        return self.weekday() == 4

    def is_saturday(self):
        """Returns ``True`` if the date is a Saturday, ``False`` otherwise."""
        return self.weekday() == 5

    def is_sunday(self):
        """Returns ``True`` if the date is a Sunday, ``False`` otherwise."""
        return self.weekday() == 6

    def is_weekend(self) -> bool:
        """Returns ``True`` if the date is a weekend day, ``False`` otherwise."""
        return self.weekday() > 4

    def next(self) -> date:
        """Returns the next day."""
        return self + datetime.timedelta(1)

    def previous(self) -> date:
        """Returns the previous day."""
        return self - datetime.timedelta(1)

    def is_mothers_day(self) -> bool:
        """Returns ``True`` if the date is Mother's Day, ``False`` otherwise."""
        from .calendar import Calendar

        return self == Calendar(self.year).mothers_day()

    def is_fathers_day(self) -> bool:
        """Returns ``True`` if the date is Father's Day, ``False`` otherwise."""
        from .calendar import Calendar

        return self == Calendar(self.year).fathers_day()

    def is_even_year(self) -> bool:
        """Returns ``True`` if the date is in an even year, ``False`` otherwise."""
        return self.year % 2 == 0

    def is_odd_year(self) -> bool:
        """Returns ``True`` if the date is in an odd year, ``False`` otherwise."""
        return not self.is_even_year()

    def is_even_week(self) -> bool:
        """Returns ``True`` if the date is in an even week, ``False`` otherwise."""
        return self.weekid() % 2 == 0

    def is_odd_week(self) -> bool:
        """Returns ``True`` if the date is in an odd week, ``False`` otherwise."""
        return not self.is_even_week()


@dataclass
class date_range:  # pylint: disable=invalid-name  # conforms to datetime.date
    """Represents a range of dates."""

    start: date
    end: date

    @classmethod
    def from_string(cls, date_range_str: str, year: int = current_year()) -> date_range:
        """Returns a new date_range from a string representation."""
        if "-" not in date_range_str:
            raise ValueError(f"invalid date range string '{date_range_str}'")
        tokens = date_range_str.split("-")
        assert len(tokens) == 2
        start, end = [date.from_string(tok, year) for tok in tokens]
        return cls(start, end)

    def __contains__(self, day: date) -> bool:
        """Returns ``True`` if the date is in the range, ``False`` otherwise."""
        return self.start <= day <= self.end

    def __iter__(self) -> Iterator[date]:
        """Returns an iterator over the dates in the range."""
        for delta in range((self.end - self.start).days + 1):
            yield self.start + datetime.timedelta(days=delta)

    def __len__(self) -> int:
        """Returns the range length in days."""
        return (self.end - self.start).days

    def aslist(self) -> list[date]:
        """Returns the list of all dates in the range."""
        return list(self)

    def ascollection(self) -> date_collection:
        """Returns a ``date_collection`` with all dates within the range."""
        return date_collection(ranges=[self])


@dataclass
class date_collection(
    collections.abc.Collection
):  # pylint: disable=invalid-name  # conforms to datetime.date
    """Stores list of dates and date ranges."""

    date_list: list[date] = field(default_factory=list)
    ranges: list[date_range] = field(default_factory=list)

    def aslist(self) -> list[date]:
        """Returns the sorted list of all dates in the collection."""
        return sorted(
            self.date_list + [date for r in self.ranges for date in r.aslist()]
        )

    def __contains__(self, day: object) -> bool:
        """Returns ``True`` if the date is in the collection, ``False`` otherwise."""
        if not isinstance(day, date):
            return False
        for _range in self.ranges:
            if day in _range:
                return True
        return day in self.date_list

    def __iter__(self) -> Iterator[date]:
        """Returns an iterator over the dates in the collection."""
        return iter(self.date_list)

    def __len__(self) -> int:
        """Returns the number of dates in the collection."""
        return sum(len(r) for r in self.ranges) + len(self.date_list)

    def __getitem__(self, key: int) -> date:
        """Returns the date at the given index."""
        return self.aslist()[key]

    def add_range(self, the_range: date_range):
        """Adds a date range to the collection."""
        self.ranges.append(the_range)

    def add_date(self, the_date: date):
        """Adds a date to the collection."""
        self.date_list.append(the_date)

    def half(self) -> date:
        """Returns the date that corresponds to half the collection."""
        delta = datetime.timedelta(len(self) / 2)
        return self[0] + delta


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


def date_description(
    description: str,
    year: int | date,
    month: Optional[int] = None,
    day: Optional[int] = None,
):
    """Returns a new ``date`` with a description."""
    if isinstance(year, int):
        assert month is not None
        assert day is not None
        obj = date(year, month, day)
    else:
        obj = year
    obj.description = description
    return obj


def paques(year: int = current_year()) -> date:
    """Returns the date of Easter Sunday."""
    return EASTER_SUNDAY[year]


def pentecote(year: int = current_year()) -> date:
    """Returns the date of Pentecote."""
    return paques(year) + datetime.timedelta(49)


def public_holidays(year: int = current_year()) -> date_collection:
    """Returns the list public holidays.

    Each date has a description.
    """
    delta = datetime.timedelta
    day_paques = paques(year)
    day_pentecote = pentecote(year)

    col = date_collection(
        [
            date_description("jour de l'an", year, 1, 1),
            date_description("fête du travail", year, 5, 1),
            date_description("armistice 2nde guerre", year, 5, 8),
            date_description("fête nationale", year, 7, 14),
            date_description("assomption", year, 8, 15),
            date_description("toussaint", year, 11, 1),
            date_description("armistice 1ère guerre", year, 11, 11),
            date_description("noël", year, 12, 25),
            date_description("pâques", day_paques),
            date_description("lundi de pâques", day_paques + delta(1)),
            date_description("ascension", day_paques + delta(39)),
            date_description("pentecôte", day_pentecote),
            date_description("lundi de pentecôte", day_pentecote + delta(1)),
        ]
    )

    return col
