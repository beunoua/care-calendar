"""Main module."""

from dataclasses import dataclass, field
import calendar
import datetime

from . import current_year


@dataclass
class Calendar:

    year: int = current_year()
    _cal: calendar.Calendar = field(init=False, repr=False, default=calendar.Calendar())

    css_class_month = "month"

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

    def iter_month_dates(self, month: int) -> datetime.date:
        """Iterate over a month dates."""
        dates = [date for date in self._cal.itermonthdates(self.year, month) if date.month == month]
        for day in dates:
            yield day

    def format_month(self, month: int) -> str:
        header = self.format_month_name(month)
        days = "\n".join(self.format_day(day) for day in self.iter_month_dates(month))
        html = f"<table><tbody>{header}\n{days}</tbody></table>"
        with open("foo.html", "wt") as f:
            print(html, file=f)
        return html

    def format_month_name(self, month: int) -> str:
        """Format the month name as an HTML table row header."""
        return f'<tr><th colspan="4" class="{self.css_class_month}">{self.month_name[month]}</th></tr>'

    def format_day(self, date: datetime.date) -> str:
        """Format a date as an HTML table row."""
        return f"<tr><td>{date.day:02d}</td><td>{self.day_abbr[date.weekday()]}</td></tr>"
