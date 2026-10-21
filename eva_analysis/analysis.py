from collections import Counter
from datetime import datetime
from itertools import accumulate

from .models import DurationCategory, Eva

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
    wanted = country.casefold()
    return sum(
        e.duration_hours
        for e in evas
        if e.country and e.country.casefold() == wanted
    )


def cumulative_series(evas: list[Eva]) -> tuple[list[datetime], list[float]]:
    """Cumulative hours across all countries; undated EVAs cannot be placed on the time axis."""
    dated = sorted((e for e in evas if e.date), key=lambda e: e.date)
    dates = [e.date for e in dated]
    totals = list(accumulate(e.duration_hours for e in dated))
    return dates, totals
