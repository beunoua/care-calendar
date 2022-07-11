from . import date

import collections
from dataclasses import dataclass, field
import datetime
from typing import Iterator


@dataclass
class date_collection(collections.abc.Collection):
    """Stores list of dates and date ranges."""

    date_list: list[date.date] = field(default_factory=list)
    ranges: list[date.date_range] = field(init=False, default_factory=list)

    def aslist(self) -> list[date.date]:
        return sorted(
            self.date_list + [date for r in self.ranges for date in r.aslist()]
        )

    def __contains__(self, d):
        for r in self.ranges:
            if d in r:
                return True
        return d in self.date_list

    def __iter__(self) -> Iterator[date.date]:
        return iter(self.all_dates)

    def __len__(self) -> int:
        return sum(len(r) for r in self.ranges) + len(self.date_list)

    def add_range(self, date_range: date.date_range):
        self.ranges.append(date_range)

    def add_date(self, date: date.date):
        self.date_list.append(date)


def public_holidays(year: int = date.current_year()) -> date_collection:
    """Returns the list public holidays.

    Each date has a description.
    """
    delta = datetime.timedelta
    paques = date.paques(year)
    pentecote = date.pentecote(year)

    col = date_collection(
        [
            date.date_description("jour de l'an", year, 1, 1),
            date.date_description("fête du travail", year, 5, 1),
            date.date_description("armistice 2nde guerre", year, 5, 8),
            date.date_description("fête nationale", year, 7, 14),
            date.date_description("assomption", year, 8, 15),
            date.date_description("toussaint", year, 11, 1),
            date.date_description("armistice 1ère guerre", year, 11, 11),
            date.date_description("noël", year, 12, 25),
            date.date_description("pâques", paques),
            date.date_description("lundi de pâques", paques + delta(1)),
            date.date_description("ascension", paques + delta(39)),
            date.date_description("pentecôte", pentecote),
            date.date_description("lundi de pentecôte", pentecote + delta(1)),
        ]
    )

    return col
