"""kaloot.feature - Feature classes for the calendar."""

from dataclasses import dataclass, field

from .custody import get_guardian
from .date import date
from .event import Event


@dataclass(kw_only=True)
class Feature:
    """Base class for features."""

    css_class: list[str] = field(default_factory=list)
    attrs: dict[str, str] = field(default_factory=dict)

    def format_attrs(self, day: date) -> str:
        """Returns the HTML attributes for the cell."""
        attrs = {}
        if self.dynamic_css_class(day):
            attrs["class"] = " ".join(self.dynamic_css_class(day))
        attrs_str = " ".join(f'{key}="{value}"' for key, value in attrs.items())
        return attrs_str

    def dynamic_css_class(self, day: date) -> list[str]:
        """Returns the dynamic CSS class for the cell."""
        return self.css_class

    def format_text(self, day: date) -> str:
        """Returns the text for the cell."""
        return ""


class TextFeature(Feature):
    """Base class for text features."""


class DayNumberFeature(TextFeature):
    """Feature for day number."""

    def format_text(self, day: date) -> str:
        return f"{day.day:02d}"


@dataclass
class DayAbbrFeature(TextFeature):
    """Feature for day abbreviation."""

    names: list[str]

    def format_text(self, day: date) -> str:
        return f"{self.names[day.weekday()]}"


@dataclass
class ColorFeature(Feature):
    """Base class for features represented as colored cells."""

    CSS_CLASS_DEFAULT = "coloredcell"

    def __post_init__(self):
        if not self.css_class:
            self.css_class = [self.CSS_CLASS_DEFAULT]

    def format_text(self, day: date) -> str:
        return "&nbsp"


@dataclass
class EventCollectionFeature(ColorFeature):
    """Feature for event collection."""

    event: Event

    def dynamic_css_class(self, day: date) -> list[str]:
        css = self.css_class.copy()
        if day in self.event.dates:
            css.append(self.event.css_class)
        return css


@dataclass
class EventCollectionFeatureMerge(ColorFeature):
    """Feature for merge event collections."""

    event_list: list[Event]

    def dynamic_css_class(self, day: date) -> list[str]:
        css = self.css_class.copy()
        for event in self.event_list:
            if day in event.dates:
                css.append(event.css_class)
        return css


def merge(event_list: list[Event]) -> EventCollectionFeatureMerge:
    """Merge several ``Event`` instances into a ``EventCollectionFeatureMerge``."""
    return EventCollectionFeatureMerge(event_list)


@dataclass
class CustodyFeature(TextFeature):
    """Feature for the children custody."""

    holidays: Event

    def __post_init__(self):
        self.css_class = ["daycust"]

    def format_text(self, day: date) -> str:
        return get_guardian(day, self.holidays.dates)
