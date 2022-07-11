from __future__ import annotations

from dataclasses import dataclass
import datetime
from typing import Union


def current_year() -> int:
    return datetime.datetime.now().year


class date(datetime.date):
    @classmethod
    def from_string(cls, date_string: str, year: int = None) -> date:
        """Returns a new `date` from a string."""
        tokens = [token.strip() for token in date_string.split("/")]
        if len(tokens) == 3:
            day, month, year = tokens
            if len(year) == 2:
                year = "20{}".format(year)
        elif len(tokens) == 2:
            year = current_year() if year is None else year
            day, month = tokens
        else:
            raise ValueError(f"Invalid date string: {date_string:!r}")
        try:
            return cls(int(year), int(month), int(day))
        except ValueError as exc:
            raise ValueError(f"day is out of range: {year}/{month}/{day}") from exc

    @classmethod
    def from_date(cls, d: datetime.date) -> date:
        return cls.fromordinal(d.toordinal())

    def astuple(self) -> tuple(int):
        return (self.year, self.month, self.day)

    def weekid(self) -> int:
        return self.isocalendar()[1]

    def is_monday(self):
        return self.weekday() == 0

    def is_tuesday(self):
        return self.weekday() == 1

    def is_wednesday(self):
        return self.weekday() == 2

    def is_thursday(self):
        return self.weekday() == 3

    def is_friday(self):
        return self.weekday() == 4

    def is_saturday(self):
        return self.weekday() == 5

    def is_sunday(self):
        return self.weekday() == 6

    def is_weekend(self) -> bool:
        return self.weekday() > 4

    def next_day(self):
        return self + datetime.timedelta(1)

    def previous_day(self):
        return self - datetime.timedelta(1)

    def is_holiday(self, holiday_list: list[date_range]) -> bool:
        for holiday in holiday_list:
            if self in holiday:
                return True
        return False

    def next_day_is_holiday(self, holiday_list: list[list[date]]) -> bool:
        return self.next_day().is_holiday(holiday_list)

    def previous_day_is_holiday(self, holiday_list: list[list[date]]) -> bool:
        return self.previous_day().is_holiday(holiday_list)

    def is_last_day_of_holidays(self, holidays: list[date]) -> bool:
        return self == holidays[-1]

    def is_mothers_day(self) -> bool:
        from .calendar import Calendar

        return self == Calendar(self.year).mothers_day()

    def is_fathers_day(self) -> bool:
        from .calendar import Calendar

        return self == Calendar(self.year).fathers_day()

    def is_even_year(self) -> bool:
        return self.year % 2 == 0

    def is_odd_year(self) -> bool:
        return not self.is_even_year()

    def is_even_week(self) -> bool:
        return self.weekid() % 2 == 0

    def is_odd_week(self) -> bool:
        return not self.is_even_week()


@dataclass
class date_range:
    start: date
    end: date

    @classmethod
    def from_string(cls, date_range_str: str, year: int = None) -> list[date]:
        """Returns a new date_range from a string representation."""
        if "-" not in date_range_str:
            raise ValueError(f"invalid date range string '{date_range_str}'")
        tokens = date_range_str.split("-")
        assert len(tokens) == 2
        start, end = [date.from_string(tok, year) for tok in tokens]
        return cls(start, end)

    def aslist(self) -> list[date]:
        """Returns the list of all dates in the range."""
        return list(self)

    def __contains__(self, day: date) -> bool:
        return self.start <= day <= self.end

    def __iter__(self):
        for delta in range((self.end - self.start).days + 1):
            yield self.start + datetime.timedelta(days=delta)


def date_description(
    description: str, year: Union[int, date], month: int = None, day: int = None
):
    if isinstance(year, int):
        assert month is not None
        assert day is not None
        obj = date(year, month, day)
    else:
        obj = year
    obj.description = description
    return obj


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


def paques(year: int = current_year()) -> date:
    return EASTER_SUNDAY[year]


def pentecote(year: int = current_year()) -> date:
    return paques(year) + datetime.timedelta(49)
