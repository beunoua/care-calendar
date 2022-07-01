from .date import date

import calendar
from dataclasses import dataclass, field
import datetime
from typing import List, Iterator


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

PENTECOST = {year: day + datetime.timedelta(49) for year, day in EASTER_SUNDAY.items()}


def current_year() -> int:
    return datetime.datetime.now().year


@dataclass
class Calendar:
    """Calendar class provides generic calendar helper functions."""

    year: int = current_year()
    _cal: calendar.Calendar = field(init=False, repr=False, default=calendar.Calendar())

    def iter_month_dates(self, month: int) -> Iterator[date]:
        """Iterates over a month dates."""
        for date in self._cal.itermonthdates(self.year, month):
            if date.month == month:
                yield date

    def iter_month_weeks(self, month: int) -> Iterator[List[date]]:
        """Iterates over a month weeks."""
        for week in self._cal.monthdatescalendar(self.year, month):
            yield [date.from_date(d) for d in week if d.month == month]

    def iter_month_dates(self, month: int) -> Iterator[date]:
        for d in self._cal.itermonthdates(self.year, month):
            if d.month == month:
                yield date(d.year, d.month, d.day)

    def month_sundays(self, month: int) -> List[date]:
        """Returns all Sundays for a given month."""
        return [d for d in self.iter_month_dates(month) if d.is_sunday()]


@dataclass
class MasterCalendar:

    year: int = current_year()
    _cal: Calendar = field(init=False, repr=False, default=None)

    css_class_legend = "legend"
    css_class_month = "month"
    css_class_month_name = "month_name"
    css_class_week_number = "weekid"
    css_class_weekend = "weekend"
    css_class_weekday = "weekday"
    css_class_day_number = "daynum"
    css_class_day_name = "dayname"
    css_class_day_status = "status"
    css_class_day_custody = "daycust"

    day_abbr = ["Lu", "Ma", "Me", "Je", "Ve", "Sa", "Di"]
    month_name = [
        "",
        "Janvier",
        "Février",
        "Mars",
        "Avril",
        "Mai",
        "Juin",
        "Juillet",
        "Août",
        "Septembre",
        "Octobre",
        "Novembre",
        "Décembre",
    ]

    def __post_init__(self):
        self._cal = Calendar(self.year)

    def render(self):
        return ""

