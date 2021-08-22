"""Main module."""

from dataclasses import dataclass

from . import current_year


@dataclass
class Calendar:

    year: int = current_year()

    def format_month(self, month: int) -> str:
        return "<table></table>"
