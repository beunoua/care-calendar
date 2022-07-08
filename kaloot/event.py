from . import collections
from . import date

from datetime import timedelta

import yaml


def read_event_yaml(path: str, year: int = None) -> list[collections.date_collection]:
    """Reads a yaml file containing events and dates (or date ranges) for each event."""
    with open(path, "rt") as f:
        data = yaml.load(f, Loader=yaml.Loader)

    events = {}
    for name, datestrlist in data.items():
        collection = collections.date_collection()
        if datestrlist is not None:
            for datestr in datestrlist:
                if datestr is None:
                    raise ValueError(f"collection: {name}: empty date string")
                if "-" in datestr:
                    collection.add_range(date.date_range.from_string(datestr))
                else:
                    collection.add_date(date.date.from_string(datestr))
        events[name] = collection

    return events


def pentecote(year: int = date.current_year()):
    return collections.EASTER_SUNDAY[year] + timedelta.delta(49)
