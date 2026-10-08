import pytest

from kaloot.custody import CustomCare, get_guardian, get_guardian_with_custom
from kaloot.date import date
from kaloot.event import parse_date_list

# 2026 school holidays, as in config-2026.yaml.
HOLIDAYS = parse_date_list(
    "Vacances scolaires",
    [
        "20/12/2025 - 04/01/2026",
        "21/02 - 08/03",
        "18/04 - 03/05",
        "04/07 - 31/08",
        "17/10 - 01/11",
        "19/12 - 03/01/2027",
    ],
    2026,
)


def make_custom(*entries: tuple[str, str]) -> CustomCare:
    data = {
        "css_class": "customcare",
        "dates": [{"dates": dates, "care": care} for dates, care in entries],
    }
    return CustomCare.from_yaml("custom", data, 2026)


def test_no_custom_is_regular_rules():
    for day in parse_date_list("", ["01/01 - 31/12"], 2026).aslist():
        assert get_guardian_with_custom(day, HOLIDAYS, None) == get_guardian(
            day, HOLIDAYS
        )


def test_custom_overrides_guardian():
    custom = make_custom(("01/01 - 04/01", "B"))
    # Without custom, L has the children on Jan 1-3.
    assert get_guardian(date(2026, 1, 2), HOLIDAYS) == "L"
    assert get_guardian_with_custom(date(2026, 1, 2), HOLIDAYS, custom) == "B"


def test_transition_at_end_of_custom_period():
    custom = make_custom(("01/01 - 04/01", "B"))
    # Monday Jan 5th is L's day, so B hands over on the last custom day.
    assert get_guardian(date(2026, 1, 5), HOLIDAYS)[0] == "L"
    assert get_guardian_with_custom(date(2026, 1, 4), HOLIDAYS, custom) == "B→L"


def test_transition_before_custom_period():
    custom = make_custom(("12/01 - 13/01", "L"))
    # Sunday Jan 11th is in an even week: B has the children.
    assert get_guardian(date(2026, 1, 11), HOLIDAYS) == "B"
    assert get_guardian_with_custom(date(2026, 1, 11), HOLIDAYS, custom) == "B→L"


def test_no_transition_when_guardian_unchanged():
    custom = make_custom(("12/01 - 13/01", "B"))
    assert get_guardian_with_custom(date(2026, 1, 11), HOLIDAYS, custom) == "B"


def test_transition_between_consecutive_custom_periods():
    custom = make_custom(("12/01", "B"), ("13/01", "L"))
    assert get_guardian_with_custom(date(2026, 1, 12), HOLIDAYS, custom) == "B→L"


def test_custom_dates_event():
    custom = make_custom(("01/01 - 04/01", "B"), ("10/02", "L"))
    assert custom.event.css_class == "customcare"
    assert len(custom.event.dates) == 5
    assert date(2026, 2, 10) in custom.event.dates


@pytest.mark.parametrize(
    "data",
    [
        {"dates": [{"dates": "01/01", "care": "B"}]},
        {"css_class": "c"},
        {"css_class": "c", "dates": ["01/01"]},
        {"css_class": "c", "dates": [{"dates": "01/01"}]},
        {"css_class": "c", "dates": [{"dates": "01/01", "care": "X"}]},
    ],
)
def test_invalid_custom_yaml(data):
    with pytest.raises((KeyError, ValueError)):
        CustomCare.from_yaml("custom", data, 2026)
