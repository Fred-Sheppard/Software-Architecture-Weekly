import argparse
import sys

import matplotlib.pyplot as plt

from .analysis import (
    category_counts,
    countries,
    cumulative_series,
    resolve_country,
    total_hours_for_country,
)
from .models import Eva
from .plotting import plot_cumulative
from .reporting import format_report, write_country_csv
from .repository import load_evas


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyse EVA durations.")
    parser.add_argument("--data", default="eva-data.json", help="EVA JSON file")
    parser.add_argument("--country", help="country to report on (prompts if omitted)")
    parser.add_argument("--csv-out", default="country_statistics.csv")
    parser.add_argument("--plot-out", default="cumulative_duration.png")
    parser.add_argument("--no-show", action="store_true", help="save the plot without displaying it")
    return parser.parse_args(argv)


def prompt_country(evas: list[Eva]) -> str:
    print("Available countries:")
    for country in countries(evas):
        print("-", country)
    return input("Enter a country: ")


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    evas = load_evas(args.data)

    country = resolve_country(evas, args.country or prompt_country(evas))
    if country is None:
        sys.exit("Country not found.")

    country_hours = total_hours_for_country(evas, country)
    print(format_report(country, country_hours, category_counts(evas)))

    write_country_csv(args.csv_out, country, country_hours)
    print(f"\nCountry statistics saved to {args.csv_out}")

    plot_cumulative(*cumulative_series(evas), out=args.plot_out)
    if not args.no_show:
        plt.show()
