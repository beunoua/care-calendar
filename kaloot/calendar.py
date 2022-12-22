from .date import current_year, date, pentecote

import calendar
from dataclasses import dataclass, field
import datetime
from typing import Iterator


@dataclass
class Calendar:
    """Calendar class provides generic calendar helper functions."""

    year: int = current_year()
    _cal: calendar.Calendar = field(init=False, repr=False, default=calendar.Calendar())

    def iter_month_weeks(self, month: int) -> Iterator[list[date]]:
        """Iterates over a month weeks."""
        for week in self._cal.monthdatescalendar(self.year, month):
            yield [date.from_date(d) for d in week if d.month == month]

    def iter_month_dates(self, month: int) -> Iterator[date]:
        """Iterates over a month dates."""
        for d in self._cal.itermonthdates(self.year, month):
            if d.month == month:
                yield date(d.year, d.month, d.day)

    def month_sundays(self, month: int) -> list[date]:
        """Returns all Sundays for a given month."""
        return [d for d in self.iter_month_dates(month) if d.is_sunday()]

    def mothers_day(self) -> date:
        """Returns the day of Mother's day.

        Mother's day is the last Sunday of May unless it is the Pentecost.
        """
        sundays = self.month_sundays(5)
        if sundays[-1] == pentecote(self.year):
            return sundays[-1] + datetime.timedelta(7)
        return sundays[-1]

    def fathers_day(self) -> date:
        """Returns the day of Father's day.

        Father's day is the 3rd Sunday of June.
        """
        return self.month_sundays(6)[2]
