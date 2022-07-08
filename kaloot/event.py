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
    css_name: str = ""
    date_list: list[date.date] = field(default_factory=list)
    ranges: list[date.date_range] = field(init=False, default_factory=list)

    def __post_init__(self):
        self.date_list = self.date_list.copy()  # copies input list
        self.css_name = self.name.lower().replace(" ", "")

    @property
    def all_dates(self) -> list[date.date]:
        return self.date_list + [date for r in self.ranges for date in r.to_list()]

    def __contains__(self, date: date.date) -> bool:
        return date in self.all_dates

    def __iter__(self) -> Iterator[date.date]:
        return iter(self.all_dates)

    def __len__(self) -> int:
        return len(self.all_dates)

    def add_range(self, date_range: date.date_range):
        self.ranges.append(date_range)

    def add_date(self, date: date.date):
        self.date_list.append(date)



@dataclass
class PublicHolidays:

    year: int = date.current_year()

    def jour_de_l_an(self) -> date:
        return date(self.year, 1, 1)

    def fete_du_travail(self) -> date:
        return date(self.year, 5, 1)

    def armistice_ww2(self) -> date:
        return date(self.year, 5, 8)

    def fete_nationale(self) -> date:
        return date(self.year, 7, 14)

    def assomption(self) -> date:
        return date(self.year, 8, 15)

    def toussaint(self) -> date:
        return date(self.year, 11, 1)

    def armistice_ww1(self) -> date:
        return date(self.year, 11, 11)

    def noel(self) -> date:
        return date(self.year, 12, 25)

    def paques(self) -> date:
        return EASTER_SUNDAY[self.year]

    def lundi_de_paques(self) -> date:
        return self.paques() + datetime.timedelta(1)

    def ascension(self) -> date:
        return self.paques() + datetime.timedelta(39)

    def pentecote(self) -> date:
        return self.paques() + datetime.timedelta(49)

    def lundi_de_pentecote(self) -> date:
        return self.pentecote() + datetime.timedelta(1)

    def _all(self):
        return [
            self.jour_de_l_an(),
            self.fete_du_travail(),
            self.armistice_ww2(),
            self.fete_nationale(),
            self.assomption(),
            self.toussaint(),
            self.armistice_ww1(),
            self.noel(),
            self.paques(),
            self.lundi_de_paques(),
            self.ascension(),
            self.pentecote(),
            self.lundi_de_pentecote(),
        ]

    def __iter__(self) -> Iterator[date]:
        all_dates = self._all()
        for d in all_dates:
            yield d

    def asdict(self):
        return {
            "jour de l'an": self.jour_de_l_an(),
            "fete du travail": self.fete_du_travail(),
            "armistice 2nde guerre": self.armistice_ww2(),
            "fête nationale": self.fete_nationale(),
            "assomption": self.assomption(),
            "toussaint": self.toussaint(),
            "armistice 1ère guerre": self.armistice_ww1(),
            "noël": self.noel(),
            "pâques": self.paques(),
            "lundi de pâques": self.lundi_de_paques(),
            "ascension": self.ascension(),
            "pentecôte": self.pentecote(),
            "lundi de pentecôte": self.lundi_de_pentecote(),
        }



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
