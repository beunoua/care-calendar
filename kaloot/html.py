
from dataclasses import dataclass, field
from typing import Optional

import bs4
import jinja2

from .feature import Feature, DayAbbrFeature, DayNumberFeature
from .calendar import Calendar
from .date import current_year, date



@dataclass
class MasterConfiguration:

    css_class: dict[str, str] = field(
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
    config: MasterConfiguration = field(default_factory=MasterConfiguration)
    _cal: Optional[Calendar] = field(init=False, repr=False, default=None)
    features: list[Feature] = field(default_factory=list)

    def __post_init__(self):
        self._cal = Calendar(self.year)
        base_features = [
            DayNumberFeature(css_class=[self.config.css_class["day_number"]]),
            DayAbbrFeature(
                css_class=[self.config.css_class["day_name"]],
                names=self.config.day_abbr,
            ),
        ]
        self.features = base_features + self.features

    def render(self):
        template = self.env.get_template("year.html.j2")
        html = template.render(cal=self)
        return html

    def format_month(self, month: int) -> str:
        template = self.env.get_template("month.html.j2")
        html = template.render(
            month_name=self.config.month_name[month],
            month_id=month,
            cal=self._cal,
            format_week=self.format_week,
        )
        soup = bs4.BeautifulSoup(html, features="html.parser")
        return soup.prettify()

    def format_week(self, week: list[date]) -> str:
        template = self.env.get_template("week.html.j2")
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
