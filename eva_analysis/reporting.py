import csv
from pathlib import Path

from .models import CountrySummary, DurationCategory


def format_report(
    country: str,
    country_hours: float,
    categories: dict[DurationCategory, int],
) -> str:
    lines = [
        "",
        "Country EVA Statistics:",
        f"{country}: {country_hours:.2f} hours",
        "",
        "EVA Duration Categories:",
    ]

    total = sum(categories.values())
    for category, count in categories.items():
        percentage = count / total * 100 if total else 0
        lines.append(f"{category.value}: {count} ({percentage:.2f}%)")

    return "\n".join(lines)


def write_country_csv(path: str | Path, country: str, hours: float) -> None:
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Country", "Total EVA Duration (hours)"])
        writer.writerow([country, f"{hours:.2f}"])


def format_comparison(
    a: CountrySummary,
    b: CountrySummary,
    start_year: int,
    end_year: int,
    leader: CountrySummary | None,
) -> str:
    lines = ["", f"EVA Comparison ({start_year}-{end_year}):"]
    for summary in (a, b):
        average = summary.average_hours
        lines += [
            "",
            f"{summary.country}:",
            f"  Total EVAs: {summary.eva_count}",
            f"  Total duration: {summary.total_hours:.2f} hours",
            f"  Average duration: {'unavailable' if average is None else f'{average:.2f} hours'}",
        ]

    lines.append("")
    if leader is None:
        lines.append(f"Result: tie, both countries have {a.total_hours:.2f} hours")
    else:
        lines.append(f"Greater total EVA duration: {leader.country}")

    return "\n".join(lines)
