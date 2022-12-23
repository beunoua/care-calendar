"""kaloot.html - HTML rendering of the calendar."""

from dataclasses import dataclass, field
from typing import Any, Optional, Iterable

import bs4
import jinja2

from .calendar import Calendar
from .date import current_year, date
from .event import Event
from .feature import CustodyFeature, Feature, DayAbbrFeature, DayNumberFeature, ColorFeature
from .feature import merge as merge_features


@dataclass
class MasterConfiguration:
    """Stores the configuration parameters for the calendar."""

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

    templates: dict[str, str] = field(
        default_factory=lambda: {
            "main": "index.html.j2",
            "year": "year.html.j2",
            "month": "month.html.j2",
            "week": "week.html.j2",
            "legend": "legend.html.j2",
        }
    )


@dataclass
class MasterCalendar:
    """Master calendar class."""

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

    def format_year(self):
        """Returns the HTML for the whole year."""
        template = self.env.get_template(self.config.templates["year"])
        html = template.render(cal=self)
        return html

    def format_month(self, month: int) -> str:
        """Returns the HTML for a specific month."""
        template = self.env.get_template(self.config.templates["month"])
        html = template.render(
            month_name=self.config.month_name[month],
            month_id=month,
            cal=self._cal,
            format_week=self.format_week,
        )
        soup = bs4.BeautifulSoup(html, features="html.parser")
        return soup.prettify()

    def format_week(self, week: list[date]) -> str:
        """Returns the HTML for a specific week."""
        template = self.env.get_template(self.config.templates["week"])
        html = template.render(
            week_id=week[0].weekid(),
            week=week,
            master=self,
        )
        return html

    def get_css_class_date(self, day: date) -> str:
        """Returns css classes for a specific day."""
        # Weekend/weekday specific classes.
        css = []
        if day.weekday() in (5, 6):
            css.append(self.config.css_class["weekend"])
        else:
            css.append(self.config.css_class["weekday"])
        css.append(self.config.day_abbr[day.weekday()].lower())
        return " ".join(css)

    def get_css_class_week_number(self) -> str:
        """Returns css classes for the week number column."""
        return self.config.css_class["week_number"]

    def format_legend(self, events: Iterable[Event]) -> str:
        """Returns the legend for the calendar."""
        template = self.env.get_template(self.config.templates["legend"])
        html = template.render(
            master=self,
            features=events,
            colored_cell_css_class=ColorFeature.CSS_CLASS_DEFAULT,
        )
        return html

    def render(self, events: Iterable[Event], comments: str) -> str:
        """Renders the whole calendar.

        Arguments:
            events: The events to display on the calendar (i.e. public & school holidays.
            comments: Comments to display on the calendar in HTML format.
        """
        template = self.env.get_template(self.config.templates["main"])
        html = template.render(
            html_legend=self.format_legend(events),
            html_calendar=self.format_year(),
            html_comments=comments,
            this_year=self.year,
        )
        return html


def render(config: dict[str, Any]):
    """Renders the calendar."""
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(config["template_search_path"]),
        autoescape=jinja2.select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    public_holidays = config["public_holidays"]
    school_holidays = config["school_holidays"]
    cal = create_calendar(env, public_holidays, school_holidays, config["year"])
    return cal.render((public_holidays, school_holidays), config["comments_html"])


def create_calendar(
    env: jinja2.Environment, public_holidays: Event, school_holidays: Event, year: int
):
    """Creates the calendar for the current year."""
    features = [
        merge_features([school_holidays, public_holidays]),
        CustodyFeature(school_holidays),
    ]
    cal = MasterCalendar(env, features=features, year=year)
    return cal
