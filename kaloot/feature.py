

from calendar import day_abbr
from dataclasses import dataclass, field
from .date import date


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



class ColorFeature(Feature):
    def format_text(self, day: date) -> str:
        return "&nbsp"



class HolidayFeature(ColorFeature):

    def dynamic_css_class(self, day: date) -> list[str]:
        return self.get_css_holiday(day)

    def get_css_holiday(self, day: date) -> list[str]:
        return ["status", "vacancesscolaires"]
