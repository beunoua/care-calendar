from hypothesis import given
from hypothesis.strategies import integers
import pytest

from kaloot.date import date, date_collection, date_range, paques


@pytest.mark.parametrize("date_string", ["1/2/3/4", "12", ""])
def test_from_string_invalid_format(date_string):
    with pytest.raises(ValueError, match="Invalid date string"):
        date.from_string(date_string, 2026)


def test_date_collection_iter_includes_ranges():
    collection = date_collection(
        date_list=[date(2026, 1, 10)],
        ranges=[date_range(date(2026, 1, 1), date(2026, 1, 3))],
    )
    assert list(collection) == [
        date(2026, 1, 1),
        date(2026, 1, 2),
        date(2026, 1, 3),
        date(2026, 1, 10),
    ]
    assert len(list(collection)) == len(collection)


EASTER_SUNDAY = {
    2021: (4, 4),
    2022: (4, 17),
    2023: (4, 9),
    2024: (3, 31),
    2025: (4, 20),
    2026: (4, 5),
    2027: (3, 28),
    2028: (4, 16),
    2029: (4, 1),
    2030: (4, 21),
    2031: (4, 13),
    2032: (3, 28),
    2033: (4, 17),
    2034: (4, 9),
    2035: (3, 25),
    2036: (4, 13),
    2037: (4, 5),
    2038: (4, 25),
    2039: (4, 10),
    2040: (4, 1),
}


@pytest.mark.parametrize("year, month_day", EASTER_SUNDAY.items())
def test_paques_known_dates(year, month_day):
    assert paques(year) == date(year, *month_day)


@given(integers(min_value=1583, max_value=9999))
def test_paques_is_sunday_in_range(year):
    day = paques(year)
    assert day.is_sunday()
    assert date(year, 3, 22) <= day <= date(year, 4, 25)
