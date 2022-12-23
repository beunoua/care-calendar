from dataclasses import dataclass, field
from .event import Event, get_public_holidays


@dataclass
class UserConfiguration:
    """Stores parameters read from the user configuration file."""

    year: int
    template_search_path: str
    comments_html: str
    school_holidays: Event
    public_holidays: Event = field(init=False)

    def __post_init__(self):
        self.public_holidays = get_public_holidays(self.year)

    @property
    def events(self) -> list[Event]:
        return [self.public_holidays, self.school_holidays]
