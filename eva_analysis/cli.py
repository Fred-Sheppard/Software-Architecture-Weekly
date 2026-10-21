import argparse
import sys
from collections.abc import Callable
from typing import TypeVar

import matplotlib.pyplot as plt

from .analysis import (
    category_counts,
    countries,
    cumulative_series,
    greater_total,
    resolve_country,
    summarize_country,
    total_hours_for_country,
    validate_period,
)
from .models import Eva
from .plotting import plot_cumulative
from .reporting import format_comparison, format_report, write_country_csv
from .repository import load_evas

T = TypeVar("T")


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyse EVA durations.")
    parser.add_argument("--data", default="eva-data.json", help="EVA JSON file")
    parser.add_argument("--country", help="country to report on (prompts if omitted)")
    parser.add_argument("--csv-out", default="country_statistics.csv")
    parser.add_argument("--plot-out", default="cumulative_duration.png")
    parser.add_argument("--no-show", action="store_true", help="save the plot without displaying it")

    commands = parser.add_subparsers(dest="command")
    compare = commands.add_parser(
        "compare",
        help="compare EVA activity between two countries over a period",
        description="Compare EVA activity between two countries. Missing values are prompted for.",
    )
    compare.add_argument("--country-a")
    compare.add_argument("--country-b")
    compare.add_argument("--start-year", help="inclusive")
    compare.add_argument("--end-year", help="inclusive")
    return parser.parse_args(argv)


def prompt_country(evas: list[Eva]) -> str:
    print_countries(evas)
    return input("Enter a country: ")


def print_countries(evas: list[Eva]) -> None:
    print("Available countries:")
    for country in countries(evas):
        print("-", country)


def obtain(value: str | None, prompt: str, convert: Callable[[str], T]) -> T:
    """Convert a command-line value, exiting if invalid, or prompt until valid input is given."""
    if value is not None:
        try:
            return convert(value)
        except ValueError as error:
            sys.exit(str(error))

    while True:
        try:
            return convert(input(prompt))
        except ValueError as error:
            print(error)
        except EOFError:
            sys.exit("\nNo input provided.")


def parse_year(text: str) -> int:
    try:
        return int(text.strip())
    except ValueError:
        raise ValueError(f"Invalid year: {text.strip()!r}.") from None


def known_country(evas: list[Eva]) -> Callable[[str], str]:
    def convert(text: str) -> str:
        country = resolve_country(evas, text)
        if country is None:
            raise ValueError(f"Unknown country: {text.strip()!r}.")
        return country

    return convert


def obtain_period(args: argparse.Namespace) -> tuple[int, int]:
    while True:
        start_year = obtain(args.start_year, "Start year: ", parse_year)
        end_year = obtain(args.end_year, "End year: ", parse_year)
        try:
            validate_period(start_year, end_year)
            return start_year, end_year
        except ValueError as error:
            if args.start_year is not None and args.end_year is not None:
                sys.exit(str(error))
            print(error)


def run_compare(args: argparse.Namespace, evas: list[Eva]) -> None:
    if args.country_a is None or args.country_b is None:
        print_countries(evas)
    country_a = obtain(args.country_a, "Country A: ", known_country(evas))
    country_b = obtain(args.country_b, "Country B: ", known_country(evas))
    start_year, end_year = obtain_period(args)

    a = summarize_country(evas, country_a, start_year, end_year)
    b = summarize_country(evas, country_b, start_year, end_year)
    print(format_comparison(a, b, start_year, end_year, greater_total(a, b)))


def run_report(args: argparse.Namespace, evas: list[Eva]) -> None:
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


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    evas = load_evas(args.data)

    if args.command == "compare":
        run_compare(args, evas)
    else:
        run_report(args, evas)
