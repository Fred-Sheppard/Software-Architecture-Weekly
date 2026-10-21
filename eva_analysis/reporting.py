import csv
from pathlib import Path

from .models import DurationCategory


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
