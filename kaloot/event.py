from __future__ import annotations

from . import date

import collections
import datetime
from dataclasses import dataclass, field
from typing import Iterator

import yaml


@dataclass
class EventCollection(collections.abc.Collection):
    """Stores the list of dates."""

    name: str
    date_list: list[date.date] = field(default_factory=list)
    css_name: str = ""
    ranges: list[date.date_range] = field(init=False, default_factory=list)

    def __post_init__(self):
        self.date_list = self.date_list.copy()  # copies input list
        self.css_name = self.name.lower().replace(" ", "")

    def __contains__(self, date: date.date) -> bool:
        return date in self.date_list

    def __iter__(self) -> Iterator[date.date]:
        return iter(self.date_list)

    def __len__(self) -> int:
        return len(self.date_list)

    def add_range(self, date_range: date.date_range):
        self.ranges.append(date_range)

    def add_date(self, date: date.date):
        self.date_list.append(date)


def read_event_yaml(path: str, year: int = None) -> list[EventCollection]:
    """Reads a yaml file containing events and dates (or date ranges) for each event."""
    with open(path, "rt") as f:
        data = yaml.load(f, Loader=yaml.Loader)

    events = []
    for name, datestrlist in data.items():
        collection = EventCollection(name.lower())
        if datestrlist is not None:
            for datestr in datestrlist:
                if datestr is None:
                    raise ValueError(f"collection: {name}: empty date string")
                if "-" in datestr:
                    collection.add_range(date.date_range.from_string(datestr))
                else:
                    collection.add_date(date.date.from_string(datestr))
        events.append(collection)

    return events
