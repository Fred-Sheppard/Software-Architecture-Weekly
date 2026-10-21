from datetime import datetime

import pytest

from eva_analysis.analysis import (
    categorize,
    category_counts,
    countries,
    cumulative_series,
    greater_total,
    resolve_country,
    summarize_country,
    total_hours_for_country,
    validate_period,
)
from eva_analysis.models import CountrySummary, DurationCategory, Eva


def eva(hours, country="USA", date=None):
    return Eva(country, date, hours)


@pytest.mark.parametrize(
    "hours, category",
    [
        (0, DurationCategory.SHORT),
        (3.99, DurationCategory.SHORT),
        (4, DurationCategory.STANDARD),
        (6.99, DurationCategory.STANDARD),
        (7, DurationCategory.LONG),
        (9, DurationCategory.LONG),
    ],
)
def test_categorize_boundaries(hours, category):
    assert categorize(eva(hours)) == category


def test_category_counts_includes_empty_categories_in_order():
    counts = category_counts([eva(1), eva(2)])
    assert list(counts.items()) == [
        (DurationCategory.SHORT, 2),
        (DurationCategory.STANDARD, 0),
        (DurationCategory.LONG, 0),
    ]


def test_countries_sorted_and_unique():
    evas = [eva(1, "USA"), eva(1, "Russia"), eva(1, None), eva(1, "USA")]
    assert countries(evas) == ["Russia", "USA"]


@pytest.mark.parametrize("query", ["usa", " USA ", "Usa"])
def test_resolve_country_is_case_and_whitespace_insensitive(query):
    assert resolve_country([eva(1, "USA")], query) == "USA"


def test_resolve_country_unknown():
    assert resolve_country([eva(1, "USA")], "France") is None


def test_total_hours_for_country_includes_undated():
    evas = [
        eva(1, "USA", datetime(2000, 1, 1)),
        eva(2, "USA"),
        eva(4, "Russia"),
        eva(8, None),
    ]
    assert total_hours_for_country(evas, "usa") == 3


def test_cumulative_series_sorts_and_skips_undated():
    evas = [
        eva(2, "Russia", datetime(2001, 1, 1)),
        eva(5, "USA"),
        eva(1, "USA", datetime(2000, 1, 1)),
    ]
    dates, totals = cumulative_series(evas)
    assert dates == [datetime(2000, 1, 1), datetime(2001, 1, 1)]
    assert totals == [1, 3]


def test_summarize_country_includes_both_boundary_years():
    evas = [
        eva(1, "USA", datetime(1999, 12, 31)),
        eva(2, "USA", datetime(2000, 1, 1)),
        eva(3, "USA", datetime(2005, 6, 1)),
        eva(4, "USA", datetime(2010, 12, 31)),
        eva(5, "USA", datetime(2011, 1, 1)),
        eva(6, "Russia", datetime(2005, 1, 1)),
        eva(7, "USA"),
    ]
    summary = summarize_country(evas, "usa", 2000, 2010)
    assert summary == CountrySummary("usa", 3, 9)
    assert summary.average_hours == 3


def test_summarize_country_single_year_period():
    evas = [eva(2, "USA", datetime(2000, 3, 1)), eva(4, "USA", datetime(2001, 3, 1))]
    assert summarize_country(evas, "USA", 2000, 2000).eva_count == 1


def test_summarize_country_with_no_matches_has_no_average():
    summary = summarize_country([eva(2, "USA", datetime(2000, 1, 1))], "Russia", 2000, 2010)
    assert summary.eva_count == 0
    assert summary.total_hours == 0
    assert summary.average_hours is None


def test_summarize_country_rejects_reversed_period():
    with pytest.raises(ValueError):
        summarize_country([], "USA", 2010, 2000)


def test_validate_period_accepts_equal_years():
    validate_period(2000, 2000)


def test_greater_total():
    a = CountrySummary("USA", 2, 10)
    b = CountrySummary("Russia", 3, 9)
    assert greater_total(a, b) is a
    assert greater_total(b, a) is a


def test_greater_total_tie_tolerates_float_error():
    a = CountrySummary("USA", 3, 0.1 + 0.2)
    b = CountrySummary("Russia", 1, 0.3)
    assert greater_total(a, b) is None


def test_greater_total_tie_when_both_empty():
    assert greater_total(CountrySummary("USA", 0, 0), CountrySummary("Russia", 0, 0)) is None
