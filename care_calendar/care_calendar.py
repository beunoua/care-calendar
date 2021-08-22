"""Main module."""

from dataclasses import dataclass, field
import calendar

from . import current_year


@dataclass
class Calendar:

    year: int = current_year()
    _cal: calendar.Calendar = field(init=False, repr=False, default=calendar.Calendar)

    def format_month(self, month: int) -> str:
        return "<table></table>"
