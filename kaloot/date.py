from __future__ import annotations

import datetime
from typing import List

class date(datetime.date):

    @classmethod
    def from_date(cls, d: datetime.date) -> date:
        return cls.fromordinal(d.toordinal())

    def weekid(self) -> int:
        return self.isocalendar()[1]

    def is_sunday(self):
        return self.weekday() == 6

    def is_weekend(self) -> bool:
        return self.weekday() > 4

    def next_day(self):
        return self + datetime.timedelta(1)

    def previous_day(self):
        return self - datetime.timedelta(1)

    def is_holiday(self, holiday_list: List[List[date]]) -> bool:
        for holiday in holiday_list:
            if self in holiday:
                return True
        return False

    def next_day_is_holiday(self, holiday_list: List[List[date]]) -> bool:
        return self.next_day().is_holiday(holiday_list)

    def previous_day_is_holiday(self, holiday_list: List[List[date]]) -> bool:
        return self.previous_day().is_holiday(holiday_list)

    def is_last_day_of_holidays(self, holidays: List[date]) -> bool:
        return self == holidays[-1]
