from kaloot.feature import Feature, DayAbbrFeature, DayNumberFeature
from .date import date

import calendar
from dataclasses import dataclass, field
import datetime
from typing import Iterator

from bs4 import BeautifulSoup as BS

import jinja2


def prettify_html(html: str) -> str:
    soup = BS(html, features="html.parser")
    return soup.prettify()


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

    def iter_month_weeks(self, month: int) -> Iterator[list[date]]:
        """Iterates over a month weeks."""
        for week in self._cal.monthdatescalendar(self.year, month):
            yield [date.from_date(d) for d in week if d.month == month]

    def iter_month_dates(self, month: int) -> Iterator[date]:
        for d in self._cal.itermonthdates(self.year, month):
            if d.month == month:
                yield date(d.year, d.month, d.day)

    def month_sundays(self, month: int) -> list[date]:
        """Returns all Sundays for a given month."""
        return [d for d in self.iter_month_dates(month) if d.is_sunday()]


@dataclass
class MasterConfiguration:

    css_class: dict[str:str] = field(
        default_factory=lambda: {
            "legend": "legend",
            "month": "month",
            "month_name": "month_name",
            "week": "week",
            "week_number": "weekid",
            "weekend": "weekend",
            "weekday": "weekday",
            "day_number": "daynum",
            "day_name": "dayname",
            "day_holiday": "holidays",
            "day_custody": "daycust",
        }
    )

    day_abbr: list[str] = field(
        default_factory=lambda: ["Lu", "Ma", "Me", "Je", "Ve", "Sa", "Di"]
    )

    month_name: dict[int, str] = field(
        default_factory=lambda: {
            1: "Janvier",
            2: "Février",
            3: "Mars",
            4: "Avril",
            5: "Mai",
            6: "Juin",
            7: "Juillet",
            8: "Août",
            9: "Septembre",
            10: "Octobre",
            11: "Novembre",
            12: "Décembre",
        }
    )


@dataclass
class MasterCalendar:

    env: jinja2.Environment
    year: int = current_year()
    config: MasterConfiguration = MasterConfiguration()
    _cal: Calendar = field(init=False, repr=False, default=None)
    features: list[Feature] = field(default_factory=list)

    def __post_init__(self):
        self._cal = Calendar(self.year)
        self.features = [
            DayNumberFeature(css_class=[self.config.css_class["day_number"]]),
            DayAbbrFeature(
                css_class=[self.config.css_class["day_name"]],
                names=self.config.day_abbr,
            ),
        ]

    def render(self):
        return self.format_month(1)

    def format_month(self, month: int) -> str:
        template = self.env.get_template("month.j2")
        html = template.render(
            month_name=self.config.month_name[month],
            month_id=month,
            cal=self._cal,
            format_week=self.format_week,
        )
        soup = BS(html, features="html.parser")
        return soup.prettify()

    def format_week(self, week: list[date]) -> str:
        template = self.env.get_template("week.j2")
        html = template.render(
            week_id=week[0].weekid(),
            week=week,
            master=self,
        )
        return html

    def format_css_day(self, day: date) -> str:
        """Returns css classes for a specific day."""
        # Weekend/weekday specific classes.
        css = []
        if day.weekday() in (5, 6):
            css.append(self.config.css_class["weekend"])
        else:
            css.append(self.config.css_class["weekday"])
        css.append(self.config.day_abbr[day.weekday()].lower())
        return " ".join(css)
