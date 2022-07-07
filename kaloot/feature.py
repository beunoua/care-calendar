

from calendar import day_abbr
from dataclasses import dataclass, field
from .date import date


@dataclass(kw_only=True)
class Feature:
    css_class: list[str] = field(default_factory=list)
    attrs: dict[str, str] = field(default_factory=dict)

    def format_attrs(self, day: date):
        attrs = {"class": " ".join(self.css_class)}
        attrs.update(self.attrs)
        attrs_str = " ".join(f'{key}="{value}"' for key, value in attrs.items())
        return attrs_str

    def format_text(self, day: date):
        return ""


class TextFeature(Feature):
    pass



class DayNumberFeature(TextFeature):
    def format_text(self, day: date):
        return f"{day.day:02d}"


@dataclass
class DayAbbrFeature(TextFeature):
    names: list[str]

    def format_text(self, day: date):
        return f"{self.names[day.weekday()]}"




class ColorFeature(Feature):
    @property
    def text(self):
        return "&nbsp"
