from datetime import datetime

import pytest

from eva_analysis.models import Eva
from eva_analysis.parsing import parse_duration, parse_eva, parse_evas


@pytest.mark.parametrize(
    "text, hours",
    [("0:00", 0.0), ("0:36", 0.6), ("6:30", 6.5), ("12:15", 12.25)],
)
def test_parse_duration(text, hours):
    assert parse_duration(text) == pytest.approx(hours)


def test_parse_eva_full_record():
    raw = {"country": "USA", "date": "1965-06-03T00:00:00.000", "duration": "0:36"}
    assert parse_eva(raw) == Eva("USA", datetime(1965, 6, 3), 0.6)


def test_parse_eva_without_date_keeps_record():
    eva = parse_eva({"country": "Russia", "duration": "2:00"})
    assert eva == Eva("Russia", None, 2.0)


def test_parse_eva_empty_country_becomes_none():
    assert parse_eva({"country": "", "duration": "1:00"}).country is None


@pytest.mark.parametrize("raw", [{}, {"duration": ""}, {"duration": "abc"}, {"duration": "1:xx"}])
def test_parse_eva_rejects_unusable_duration(raw):
    assert parse_eva(raw) is None


def test_parse_evas_drops_rejects():
    records = [{"duration": "1:00"}, {"duration": ""}, {"duration": "2:00"}]
    assert [e.duration_hours for e in parse_evas(records)] == [1.0, 2.0]
