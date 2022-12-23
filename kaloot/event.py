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
    def from_yaml(cls, name: str,  event_data: dict[str, Any], year: int = date.current_year()) -> Event:
        """Creates an Event from a YAML event data tuple.

        Arguments:
            name: The event name.
            event_data: A tuple containing the css class and a list of dates.
            year: The year of the event. This is necessay when dates are formatted
                without a year.
        """
        def parse_date_list(datestrlist: str) -> date.date_collection:
            collection = date.date_collection()
            for datestr in datestrlist:

                if datestr is None:
                    raise ValueError(f"collection: {name}: empty date string")
                if "-" in datestr:
                    collection.add_range(date.date_range.from_string(datestr, year))
                else:
                    collection.add_date(date.date.from_string(datestr, year))
            return collection

        if "css_class" not in event_data:
            raise KeyError(f"Misformatted event '{name}': missing required field 'css_class'")

        if "dates" not in event_data:
            raise KeyError(f"Misformatted event '{name}': missing required field 'dates'")

        return cls(name, event_data["css_class"], parse_date_list(event_data["dates"]))


def get_public_holidays(
    year: int, name: str = "férié", css_class: str = "férié"
) -> Event:
    """Returns a public holiday event for the given year."""
    return Event(name, css_class, date.public_holidays(year))
