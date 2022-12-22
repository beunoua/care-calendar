"""kaloot.event - Event class and related functions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from . import date


@dataclass
class Event:
    """Event class.

    An event is a named collection of dates.
    It also has a CSS class name associated with it.
    """

    name: str
    css_class: str
    dates: date.date_collection

    @classmethod
    def from_yaml(cls, event_data: tuple[str, dict[str, Any]]) -> Event:
        """Creates an Event from a YAML event data tuple."""

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
        return cls(name, data["css_class"], parse_date_list(data["dates"]))


def get_public_holidays(
    year: int, name: str = "férié", css_class: str = "férié"
) -> Event:
    """Returns a public holiday event for the given year."""
    return Event(name, css_class, date.public_holidays(year))
