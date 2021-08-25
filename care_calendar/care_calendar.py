"""Main module."""

from dataclasses import dataclass, field, make_dataclass
import calendar
import datetime
from datetime import timedelta
from typing import Iterator, List

from . import current_year, week_id
from .status import Status

@dataclass
class Calendar:

    year: int = current_year()
    status_list: List[Status] = field(default_factory=list)
    _cal: calendar.Calendar = field(init=False, repr=False, default=calendar.Calendar())

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

    @property
    def holidays(self):
        for status in self.status_list:
            if status.name == "vacances scolaires":
                return status
        return []

    def iter_month_dates(self, month: int) -> datetime.date:
        """Iterates over a month dates."""
        dates = [
            date
            for date in self._cal.itermonthdates(self.year, month)
            if date.month == month
        ]
        for day in dates:
            yield day

    def iter_month_weeks(self, month: int) -> Iterator[List[datetime.date]]:
        """Iterates over a month weeks."""
        weeks = [
            [date for date in week if date.month == month]
            for week in self._cal.monthdatescalendar(self.year, month)
        ]
        for week in weeks:
            yield week

    def format_month(self, month: int) -> str:
        """Formats a month as a HTML table."""
        header = self.format_month_name(month)
        weeks = "\n".join(
            self.format_week(week) for week in self.iter_month_weeks(month)
        )
        html = f'<table class="{self.css_class_month}"><tbody>{header}\n{weeks}</tbody></table>'
        return html

    def format_month_name(self, month: int) -> str:
        """Formats the month name as an HTML table row header."""
        return f'<tr class={self.css_class_month_name}><th colspan="5" class="{self.css_class_month_name}">{self.month_name[month]}</th></tr>'

    def format_week(self, dates: List[datetime.date]) -> str:
        """Formats a full week has part of an HTML table."""
        rowspan = len(dates)
        weekid = week_id(dates[0])
        week_id_html = self.format_week_number(dates[0], rowspan)
        days = [self.format_day(day) for day in dates]
        # Remove <tr> from first day.
        days[0] = days[0][days[0].find(">") + 1 :]
        return "\n".join([week_id_html] + days)

    def format_css_day(self, day: datetime.date) -> str:
        """Returns css classes for a specific day."""
        # Weekend/weekday specific classes.
        css = []
        if day.weekday() in (5, 6):
            css.append(self.css_class_weekend)
        else:
            css.append(self.css_class_weekday)
        css.append(self.day_abbr[day.weekday()].lower())
        return " ".join(css)

    def format_css_status_day(self, day: datetime.date) -> str:
        """Returns status specific css classes for a specific day."""
        css = [self.css_class_day_status]
        for status in self.status_list:
            if day in status:
                css.append(status.css_name)
        return " ".join(css)

    def format_week_number(self, date: datetime.date, rowspan: int) -> str:
        """Formats week number as the first cell of a row."""
        return (
            f"""<tr class="{self.format_css_day(date)}">"""
            f'<td rowspan="{rowspan}" '
            f'class="{self.css_class_week_number}">{week_id(date)}</td>'
        )

    def format_day(self, date: datetime.date) -> str:
        """Formats a date as an HTML table row."""
        return (
            f'<tr class="{self.format_css_day(date)}">'
            f"{self.format_day_number(date)}"
            f"{self.format_day_name(date)}"
            f"{self.format_day_status(date)}"
            f"{self.format_day_custody(date)}"
            "</tr>"
        )

    def format_day_number(self, date: datetime.date) -> str:
        """Formats the cell that contains the day number."""
        return f'<td class="{self.css_class_day_number}">{date.day:02d}</td>'

    def format_day_name(self, date: datetime.date) -> str:
        """Formats the cell that contains the day namer."""
        return f'<td class="{self.css_class_day_name}">{self.day_abbr[date.weekday()]}</td>'

    def format_day_status(self, date: datetime.date) -> str:
        """Formats the cell that contains the day status (i.e. nothing, holidays, etc.)."""
        return f'<td class="{self.format_css_status_day(date)}">&nbsp;</td>'

    def format_day_custody(self, date: datetime.date) -> str:
        """Formats the cell that contains the custody responsible."""
        return f'<td class="{self.css_class_day_custody}">{self.get_custody(date)}</td>'

    def format_year(self):
        year_html = ['<table class="year">', "<tbody>", '<tr class="year">']
        for month in range(1, 13):
            year_html.append(f'<td class="{self.css_class_month}">')
            year_html.append(self.format_month(month))
            year_html.append("</td>")
        year_html += ["</tr>", "</tbody>", "</table>"]
        return "\n".join(year_html)

    def get_custody(self, date: datetime.date) -> str:
        """Returns who's got the children custody."""
        cust = "B"
        week_is_even =  week_id(date) % 2 == 0
        if date in self.holidays:
            return self._get_custody_holidays(date)
        if date + timedelta(1) in self.holidays:
            return self._get_custody_holidays(date + timedelta(1))
        if week_is_even:
            cust = self._get_custody_even_weeks(date)
        else:
            cust = self._get_custody_odd_weeks(date)
        return cust


    def _get_custody_even_weeks(self, date: datetime.date) -> str:
        """Returns who's got the childen custody during even weeks."""
        cust = "L"
        # B has the children on Tuesday nights.
        if date.weekday() == 1:
            cust = "L/B"
        # B has the children on Wednesdays and got them back on Fridays.
        if date.weekday() == 2 or date.weekday() > 3:
            cust = "B"
        return cust

    def _get_custody_odd_weeks(self, date: datetime.date) -> str:
        """Returns who's got the childen custody during odd weeks."""
        cust = "B"
        # L got the children back on Fridays.
        if date.weekday() > 3:
            cust = "L"
        return cust

    def _get_custody_holidays(self, date: datetime.date) -> str:
        """Returns who's got the children custody during holidays."""
        year_is_even =  date.year % 2 == 0
        holidays = [r for r in self.holidays.ranges if date in r][0]
        # date is in first half of holidays
        delta = timedelta(len(holidays) / 2)
        is_first_half = date < holidays[0] + delta

        if year_is_even:
            if is_first_half:
                return "L"
            return "B"
        elif is_first_half:
                return "B"  
        return "L"