"""care.calendar day status.

Status is essentially a day that will have a specific css
so that it will be displayed in a specific fashion.
"""

import collections
from dataclasses import dataclass, field
import datetime
from typing import List, Iterator
import yaml

from .utils import current_year


@dataclass
class Status(collections.abc.Collection):
    """Stores the list of dates that will be assigned a particular status."""

    name: str
    date_list: List[datetime.time] = field(default_factory=list)
    css_name: str = ""
    ranges: List[List[List[datetime.time]]] = field(
        init=False, repr=False, default_factory=list
    )

    def __post_init__(self):
        self.date_list = self.date_list.copy()  # copies input list
        self.css_name = self.name.lower().replace(" ", "")

    def __contains__(self, date: datetime.date) -> bool:
        return date in self.date_list

    def __iter__(self) -> Iterator[datetime.date]:
        return iter(self.date_list)

    def __len__(self) -> int:
        return len(self.date_list)

    def add_range(self, date_range: List[datetime.time]):
        self.ranges.append(date_range.copy())


def str_to_date(date_string: str, year: int = None) -> datetime.date:
    """Returns a `datetime.date` from a string."""
    tokens = [token.strip() for token in date_string.split("/")]
    if len(tokens) == 3:
        if year is not None:
            raise ValueError(
                f"Cannot pass year in date string ({date_string}) and as argument ({year})"
            )
        day, month, year = tokens
        if len(year) == 2:
            year = "20{}".format(year)
    elif len(tokens) == 2:
        year = current_year() if year is None else year
        day, month = tokens
    else:
        raise ValueError(f"Invalid date string: {date_string:!r}")
    try:
        return datetime.date(int(year), int(month), int(day))
    except ValueError as exc:
        raise ValueError(f"day is out of range: {year}/{month}/{day}") from exc


def date_range_from_str(daterange: str, year: int = None) -> List[datetime.date]:
    """Returns a list of dates from a string representing a date range."""
    start, end = [str_to_date(s, year) for s in daterange.split("-")]
    return date_range(start, end)


def date_range(start: datetime.date, end: datetime.date) -> List[datetime.date]:
    """Returns a list of dates between two dates."""
    return [start + datetime.timedelta(days=i) for i in range((end - start).days + 1)]


def read_status_yaml(path: str, year: int = None):
    """Reads a yaml file containing categories and date ranges for each categories."""
    with open(path, "rt") as f:
        data = yaml.load(f, Loader=yaml.Loader)

    categories = []
    for category, datestrlist in data.items():
        status = Status(category.lower())
        if datestrlist is not None:
            for datestr in datestrlist:
                if datestr is None:
                    raise ValueError(f"category: {category}: empty date string")
                # date is a range.
                if "-" in datestr:
                    dates = date_range(datestr, year_from_str)
                    status.add_range(dates)
                    status.date_list.extend(dates)
                else:
                    status.date_list.append(str_to_date(datestr, year))

        categories.append(status)

    return categories
