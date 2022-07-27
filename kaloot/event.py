from __future__ import annotations

from . import date

from dataclasses import dataclass
from typing import Any

import yaml


@dataclass
class Event:
    name: str
    css_class: str
    dates: date.date_collection

    @classmethod
    def from_yaml(self, event_data: dict[str, Any]) -> Event:
        def assert_field_present(key: str) -> None:
            if key not in data:
                raise KeyError(
                    f"Misformatted event '{name}': missing required field '{key}'"
                )

        def parse_date_list(datestrlist: str) -> date.date_collection:
            collection = date.date_collection()
            for datestr in datestrlist:

                if datestr is None:
                    raise ValueError(f"collection: {name}: empty date string")
                if "-" in datestr:
                    collection.add_range(date.date_range.from_string(datestr))
                else:
                    collection.add_date(date.date.from_string(datestr))
            return collection

        name, data = event_data
        assert_field_present("css_class")
        assert_field_present("dates")
        return Event(name, data["css_class"], parse_date_list(data["dates"]))


def read_event_yaml(path: str, year: int = None) -> dict[date.date_collection]:
    """Reads a yaml file containing events and dates (or date ranges) for each event."""
    with open(path, "rt") as f:
        data = yaml.load(f, Loader=yaml.Loader)

    events = {}
    for data in data.items():
        e = Event.from_yaml(data)
        events[e.name] = e
    return events


def public_holidays(name: str = "férié", css_class: str = "férié") -> Event:
    return Event(name, css_class, date.public_holidays())
