import json
from datetime import datetime

import pytest

from eva_analysis.models import Eva
from eva_analysis.plotting import plot_cumulative
from eva_analysis.repository import load_evas


def test_load_evas_parses_records_and_drops_unusable(tmp_path):
    path = tmp_path / "evas.json"
    path.write_text(json.dumps([
        {"country": "USA", "date": "2000-01-01T00:00:00.000", "duration": "1:30"},
        {"country": "Russia", "duration": "2:00"},
        {"country": "USA", "date": "2001-01-01T00:00:00.000"},
        {"country": "USA", "duration": "bad"},
    ]), encoding="utf-8")

    assert load_evas(path) == [
        Eva("USA", datetime(2000, 1, 1), 1.5),
        Eva("Russia", None, 2.0),
    ]


def test_load_evas_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_evas(tmp_path / "missing.json")


def test_plot_cumulative_saves_labelled_chart(tmp_path):
    out = tmp_path / "plot.png"
    dates = [datetime(2000, 1, 1), datetime(2001, 1, 1)]

    figure = plot_cumulative(dates, [1.0, 3.0], out)

    assert out.stat().st_size > 0
    axes = figure.axes[0]
    assert axes.get_xlabel() == "Year"
    assert axes.get_ylabel() == "Cumulative EVA duration (hours)"
    assert list(axes.lines[0].get_ydata()) == [1.0, 3.0]
