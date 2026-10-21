from eva_analysis.models import CountrySummary, DurationCategory
from eva_analysis.reporting import format_comparison, format_report, write_country_csv


def test_format_report():
    categories = {
        DurationCategory.SHORT: 1,
        DurationCategory.STANDARD: 2,
        DurationCategory.LONG: 1,
    }
    assert format_report("USA", 12.345, categories) == "\n".join([
        "",
        "Country EVA Statistics:",
        "USA: 12.35 hours",
        "",
        "EVA Duration Categories:",
        "Short: 1 (25.00%)",
        "Standard: 2 (50.00%)",
        "Long: 1 (25.00%)",
    ])


def test_format_report_with_no_classified_evas():
    categories = dict.fromkeys(DurationCategory, 0)
    report = format_report("USA", 0, categories)
    assert "Short: 0 (0.00%)" in report
    assert "Long: 0 (0.00%)" in report


def test_write_country_csv(tmp_path):
    path = tmp_path / "stats.csv"
    write_country_csv(path, "Russia", 9.5)
    assert path.read_bytes() == b"Country,Total EVA Duration (hours)\r\nRussia,9.50\r\n"


def test_format_comparison_with_leader():
    a = CountrySummary("USA", 2, 13)
    b = CountrySummary("Russia", 1, 4)
    assert format_comparison(a, b, 2000, 2010, a) == "\n".join([
        "",
        "EVA Comparison (2000-2010):",
        "",
        "USA:",
        "  Total EVAs: 2",
        "  Total duration: 13.00 hours",
        "  Average duration: 6.50 hours",
        "",
        "Russia:",
        "  Total EVAs: 1",
        "  Total duration: 4.00 hours",
        "  Average duration: 4.00 hours",
        "",
        "Greater total EVA duration: USA",
    ])


def test_format_comparison_empty_country_and_tie():
    a = CountrySummary("USA", 0, 0)
    b = CountrySummary("Russia", 0, 0)
    report = format_comparison(a, b, 1950, 1960, None)
    assert report.count("Average duration: unavailable") == 2
    assert report.endswith("Result: tie, both countries have 0.00 hours")
