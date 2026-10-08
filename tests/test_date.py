import pytest

from kaloot.date import date, date_collection, date_range


@pytest.mark.parametrize("date_string", ["1/2/3/4", "12", ""])
def test_from_string_invalid_format(date_string):
    with pytest.raises(ValueError, match="Invalid date string"):
        date.from_string(date_string)


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
