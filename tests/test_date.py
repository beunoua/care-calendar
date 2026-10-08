import pytest

from kaloot.date import date


@pytest.mark.parametrize("date_string", ["1/2/3/4", "12", ""])
def test_from_string_invalid_format(date_string):
    with pytest.raises(ValueError, match="Invalid date string"):
        date.from_string(date_string)
