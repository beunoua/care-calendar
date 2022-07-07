from __future__ import annotations

from dataclasses import dataclass
import datetime


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

    def is_holiday(self, holiday_list: list[list[date]]) -> bool:
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

    def to_list(self) -> list[date]:
        """Returns a list of all days in the range."""
        return list(self)

    def __contains__(self, day: date) -> bool:
        return self.start <= day <= self.end

    def __iter__(self):
        for delta in range((self.end - self.start).days + 1):
            yield self.start + datetime.timedelta(days=delta)