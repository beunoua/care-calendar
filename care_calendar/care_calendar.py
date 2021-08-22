"""Main module."""

from dataclasses import dataclass, field
import calendar
import datetime
from typing import Iterator, List

from . import current_year, week_id


@dataclass
class Calendar:

    year: int = current_year()
    _cal: calendar.Calendar = field(init=False, repr=False, default=calendar.Calendar())

    css_class_month = "month"
    css_class_week_number = "weekid"
    css_class_day_number = "daynum"
    css_class_day_name = "dayname"
    css_class_day_status_blank = "noday"
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

    def iter_month_dates(self, month: int) -> datetime.date:
        """Iterate over a month dates."""
        dates = [
            date
            for date in self._cal.itermonthdates(self.year, month)
            if date.month == month
        ]
        for day in dates:
            yield day

    def iter_month_weeks(self, month: int) -> Iterator[List[datetime.date]]:
        """Iterate over a month weeks."""
        weeks = [
            [date for date in week if date.month == month]
            for week in self._cal.monthdatescalendar(self.year, month)
        ]
        for week in weeks:
            yield week

    def format_month(self, month: int) -> str:
        header = self.format_month_name(month)
        weeks = "\n".join(
            self.format_week(week) for week in self.iter_month_weeks(month)
        )
        html = f"<table><tbody>{header}\n{weeks}</tbody></table>"
        with open("foo.html", "wt") as f:
            print(html, file=f)
        return html

    def format_month_name(self, month: int) -> str:
        """Format the month name as an HTML table row header."""
        return f'<tr><th colspan="5" class="{self.css_class_month}">{self.month_name[month]}</th></tr>'

    def format_week(self, dates: List[datetime.date]) -> str:
        rowspan = len(dates)
        weekid = week_id(dates[0])
        week_id_html = self.format_week_number(weekid, rowspan)
        days = [self.format_day(day) for day in dates]
        # Remove <tr> from first day.
        days[0] = days[0].replace("<tr>", "")
        return "\n".join([week_id_html] + days)

    def format_week_number(self, weekid, rowspan):
        return f'<tr><td rowspan="{rowspan}" class="{self.css_class_week_number}">{weekid}</td>'

    def format_day(self, date: datetime.date) -> str:
        """Format a date as an HTML table row."""
        return (
            "<tr>"
            f"{self.format_day_number(date)}"
            f"{self.format_day_name(date)}"
            f"{self.format_day_status(date)}"
            f"{self.format_day_custody(date)}"
            "</tr>"
        )

    def format_day_number(self, date: datetime.date) -> str:
        """Format the cell that contains the day number."""
        return f'<td class="{self.css_class_day_number}">{date.day:02d}</td>'

    def format_day_name(self, date: datetime.date) -> str:
        """Format the cell that contains the day namer."""
        return f'<td class="{self.css_class_day_name}">{self.day_abbr[date.weekday()]}</td>'

    def format_day_status(self, date: datetime.date) -> str:
        """Format the cell that contains the day status (i.e. nothing, holidays, etc.)."""
        return f'<td class="{self.css_class_day_status_blank}">&nbsp;</td>'

    def format_day_custody(self, date: datetime.date) -> str:
        """Format the cell that contains the custody responsible."""
        return f'<td class="{self.css_class_day_custody}">non</td>'
