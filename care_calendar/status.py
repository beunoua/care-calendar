"""care.calendar day status.

Status is essentially a day that will have a specific css
so that it will be displayed in a specific fashion.
"""

import datetime
from typing import List
import yaml

from .utils import current_year


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


def date_range_to_list(
    daterange: tuple[str, str], year: int = None
) -> List[datetime.date]:
    """Returns a list of dates from a string representing a date range."""
    start, end = [str_to_date(s, year) for s in daterange.split("-")]
    print(f"{start=}")
    print(f"{end=}")
    print(f"{end - start}")
    return [start + datetime.timedelta(days=i) for i in range((end - start).days + 1)]


def read_status_yaml(path: str, year: int = None):
    """Reads a yaml file containing categories and date ranges for each categories."""
    with open(path, "rt") as f:
        data = yaml.load(f, Loader=yaml.Loader)

    categories = {}
    for category, datestrlist in data.items():
        datelist = []
        if datestrlist is not None:
            for datestr in datestrlist:
                if datestr is None:
                    raise ValueError(f"category: {category}: empty date string")
                if "-" in datestr:
                    # date is a range.
                    datelist.extend(date_range_to_list(datestr, year))
                else:
                    datelist.append(str_to_date(datestr, year))
        categories[category.lower()] = set(datelist)

    return categories
