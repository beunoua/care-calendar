from __future__ import annotations

from . import date

import collections
import datetime
from dataclasses import dataclass, field
from typing import Iterator

import yaml

EASTER_SUNDAY = {
    2021: date.date(2021, 4, 4),
    2022: date.date(2022, 4, 17),
    2023: date.date(2023, 4, 9),
    2024: date.date(2024, 3, 31),
    2025: date.date(2025, 4, 20),
    2026: date.date(2026, 4, 5),
    2027: date.date(2027, 3, 28),
    2028: date.date(2028, 4, 16),
    2029: date.date(2029, 4, 1),
    2030: date.date(2030, 4, 21),
    2031: date.date(2031, 4, 13),
    2032: date.date(2032, 3, 28),
    2033: date.date(2033, 4, 17),
    2034: date.date(2034, 4, 9),
    2035: date.date(2035, 3, 25),
    2036: date.date(2036, 4, 13),
    2037: date.date(2037, 4, 5),
    2038: date.date(2038, 4, 25),
    2039: date.date(2039, 4, 10),
    2040: date.date(2040, 4, 1),
}


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

    def jour_de_l_an(self) -> date.named_date:
        return date.named_date("noël", date.date(self.year, 1, 1))

    def fete_du_travail(self) -> date.named_date:
        return date.named_date("fête du travail", date.date(self.year, 5, 1))

    def armistice_ww2(self) -> date.named_date:
        return date.named_date("armistice 2nde guerre", date.date(self.year, 5, 8))

    def fete_nationale(self) -> date.named_date:
        return date.named_date("fête nationale", date.date(self.year, 7, 14))

    def assomption(self) -> date.named_date:
        return date.named_date("assomption", date.date(self.year, 8, 15))

    def toussaint(self) -> date.named_date:
        return date.named_date("toussaint", date.date(self.year, 11, 1))

    def armistice_ww1(self) -> date.named_date:
        return date.named_date("armistice 1ère guerre", date.date(self.year, 11, 11))

    def noel(self) -> date.named_date:
        return date.named_date("noël", date.date(self.year, 12, 25))

    def paques(self) -> date.named_date:
        return date.named_date("pâques", EASTER_SUNDAY[self.year])

    def lundi_de_paques(self) -> date.named_date:
        return date.named_date("lundi de pâques", self.paques().date + datetime.timedelta(1))

    def ascension(self) -> date.named_date:
        return date.named_date("ascension", self.paques().date + datetime.timedelta(39))

    def pentecote(self) -> date.named_date:
        return date.named_date("pentecôte", self.paques().date + datetime.timedelta(49))

    def lundi_de_pentecote(self) -> date.named_date:
        return date.named_date("lundi de pentecôte", self.pentecote().date + datetime.timedelta(1))

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

    def __iter__(self) -> Iterator[date.named_date]:
        all_dates = self._all()
        for d in all_dates:
            yield d

    def asdict(self):
        return {date.name: date.date for date in self._all()}


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


def paques(year: int) -> date.date:
    return PublicHolidays(year).paques()


def lundi_de_paques(year: int) -> date.date:
    return PublicHolidays(year).lundi_de_paques()


def pentecote(year: int) -> date.date:
    return PublicHolidays(year).pentecote()


def lundi_de_pentecote(year: int) -> date.date:
    return PublicHolidays(year).lundi_de_pentecote()
