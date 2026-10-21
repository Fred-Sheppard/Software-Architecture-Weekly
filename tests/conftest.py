import json

import matplotlib
import pytest

matplotlib.use("Agg")

SAMPLE_RECORDS = [
    {"country": "USA", "date": "2000-03-01T00:00:00.000", "duration": "2:00"},
    {"country": "USA", "date": "2001-06-01T00:00:00.000", "duration": "5:30"},
    {"country": "USA", "date": "2010-01-01T00:00:00.000", "duration": "2:00"},
    {"country": "USA", "duration": "8:00"},
    {"country": "USA", "date": "2002-01-01T00:00:00.000"},
    {"country": "Russia", "date": "2000-01-01T00:00:00.000", "duration": "6:00"},
    {"country": "Russia", "date": "2005-01-01T00:00:00.000", "duration": "1:30"},
    {"country": "Russia", "date": "2010-06-01T00:00:00.000", "duration": "2:00"},
]


@pytest.fixture
def workdir(tmp_path, monkeypatch):
    """A working directory containing a small EVA dataset as eva-data.json."""
    (tmp_path / "eva-data.json").write_text(json.dumps(SAMPLE_RECORDS), encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    return tmp_path
