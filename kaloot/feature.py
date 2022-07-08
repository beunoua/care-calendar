from calendar import day_abbr
from dataclasses import dataclass, field

from .date import date
from .event import EventCollection


@dataclass(kw_only=True)
class Feature:
    css_class: list[str] = field(default_factory=list)
    attrs: dict[str, str] = field(default_factory=dict)

    def format_attrs(self, day: date) -> str:
        attrs = {"class": " ".join(self.dynamic_css_class(day))}
        attrs.update(self.attrs)
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
    collection: EventCollection

    def dynamic_css_class(self, day: date) -> list[str]:
        css = self.css_class.copy()
        if day in self.collection:
            css.append(self.collection.css_name)
        return css


@dataclass
class EventCollectionFeatureMerge(ColorFeature):
    collection_list: list[EventCollection]

    def dynamic_css_class(self, day: date) -> list[str]:
        css = self.css_class.copy()
        for col in self.collection_list:
            if day in col:
                css.append(col.css_name)
        return css
