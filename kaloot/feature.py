

from .custody import get_guardian
from .date import date, date_collection
from .event import Event

from dataclasses import dataclass, field


@dataclass(kw_only=True)
class Feature:
    css_class: list[str] = field(default_factory=list)
    attrs: dict[str, str] = field(default_factory=dict)

    def format_attrs(self, day: date) -> str:
        attrs = {}
        if self.dynamic_css_class(day):
            attrs["class"] = " ".join(self.dynamic_css_class(day))
        attrs_str = " ".join(f'{key}="{value}"' for key, value in attrs.items())
        return attrs_str

    def dynamic_css_class(self, day: date) -> list[str]:
        return self.css_class

    def format_text(self, day: date) -> str:
        return ""


class TextFeature(Feature):
    pass


class DayNumberFeature(TextFeature):
    def format_text(self, day: date) -> str:
        return f"{day.day:02d}"


@dataclass
class DayAbbrFeature(TextFeature):
    names: list[str]

    def format_text(self, day: date) -> str:
        return f"{self.names[day.weekday()]}"


@dataclass
class ColorFeature(Feature):
    def __post_init__(self):
        self.css_class = ["coloredcell"]

    def format_text(self, day: date) -> str:
        return "&nbsp"


@dataclass
class EventCollectionFeature(ColorFeature):
    event: Event

    def dynamic_css_class(self, day: date) -> list[str]:
        css = self.css_class.copy()
        if day in self.collection:
            css.append(self.event.css_class)
        return css


@dataclass
class EventCollectionFeatureMerge(ColorFeature):
    event_list: list[Event]

    def dynamic_css_class(self, day: date) -> list[str]:
        css = self.css_class.copy()
        for event in self.event_list:
            if day in event.dates:
                css.append(event.css_class)
        return css


def merge(event_list: list[Event]) -> EventCollectionFeatureMerge:
    return EventCollectionFeatureMerge(event_list)


@dataclass
class CustodyFeature(TextFeature):
    holidays: date_collection

    def __post_init__(self):
        self.css_class = ["daycust"]

    def format_text(self, day: date) -> str:
        return get_guardian(day, self.holidays)
