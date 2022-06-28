
import calendar
from dataclasses import dataclass, field
import datetime
from typing import List, Iterator

def current_year() -> int:
    return datetime.datetime.now().year


@dataclass
class Calendar:
    """Calendar classe provides generic calendar helper functions."""
    year: int = current_year()
    _cal: calendar.Calendar = field(init=False, repr=False, default=calendar.Calendar())

    def iter_month_dates(self, month: int) -> Iterator[datetime.date]:
        """Iterates over a month dates."""
        for date in self._cal.itermonthdates(self.year, month):
            if date.month == month:
                yield date

    def iter_month_weeks(self, month: int) -> Iterator[List[datetime.date]]:
        """Iterates over a month weeks."""
        for week in self._cal.monthdatescalendar(self.year, month):
            yield [date for date in week if date.month == month]



@dataclass
class MasterCalendar:

    year: int = current_year()
    # status_list: List[Status] = field(default_factory=list)
    # first_month: int = 1
    # _cal: calendar.Calendar = field(init=False, repr=False, default=calendar.Calendar())

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



