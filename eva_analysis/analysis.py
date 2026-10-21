from collections import Counter
from datetime import datetime
from itertools import accumulate
from math import isclose

from .models import CountrySummary, DurationCategory, Eva

SHORT_LIMIT_HOURS = 4
STANDARD_LIMIT_HOURS = 7


def categorize(eva: Eva) -> DurationCategory:
    if eva.duration_hours < SHORT_LIMIT_HOURS:
        return DurationCategory.SHORT
    if eva.duration_hours < STANDARD_LIMIT_HOURS:
        return DurationCategory.STANDARD
    return DurationCategory.LONG


def category_counts(evas: list[Eva]) -> dict[DurationCategory, int]:
    counts = Counter(categorize(e) for e in evas)
    return {category: counts[category] for category in DurationCategory}


def countries(evas: list[Eva]) -> list[str]:
    return sorted({e.country for e in evas if e.country})


def resolve_country(evas: list[Eva], query: str) -> str | None:
    by_folded = {c.casefold(): c for c in countries(evas)}
    return by_folded.get(query.strip().casefold())


def total_hours_for_country(evas: list[Eva], country: str) -> float:
    """Includes undated EVAs, since their time still counts towards the total."""
    return sum(e.duration_hours for e in evas if _is_from(e, country))


def _is_from(eva: Eva, country: str) -> bool:
    return eva.country is not None and eva.country.casefold() == country.casefold()


def validate_period(start_year: int, end_year: int) -> None:
    if start_year > end_year:
        raise ValueError(f"Start year {start_year} is after end year {end_year}.")


def summarize_country(
    evas: list[Eva], country: str, start_year: int, end_year: int
) -> CountrySummary:
    """Inclusive of both years; undated EVAs cannot be placed in a period and are excluded."""
    validate_period(start_year, end_year)
    matching = [
        e for e in evas
        if _is_from(e, country) and e.date and start_year <= e.date.year <= end_year
    ]
    return CountrySummary(
        country=country,
        eva_count=len(matching),
        total_hours=sum(e.duration_hours for e in matching),
    )


def greater_total(a: CountrySummary, b: CountrySummary) -> CountrySummary | None:
    """Return the summary with more hours, or None for a tie."""
    # Totals are sums of minutes/60, so exact float equality is unreliable
    if isclose(a.total_hours, b.total_hours, abs_tol=1e-9):
        return None
    return a if a.total_hours > b.total_hours else b


def cumulative_series(evas: list[Eva]) -> tuple[list[datetime], list[float]]:
    """Cumulative hours across all countries; undated EVAs cannot be placed on the time axis."""
    dated = sorted((e for e in evas if e.date), key=lambda e: e.date)
    dates = [e.date for e in dated]
    totals = list(accumulate(e.duration_hours for e in dated))
    return dates, totals
