from datetime import datetime

from .models import Eva


def parse_duration(text: str) -> float:
    """Convert an "H:MM" duration to hours."""
    hours, minutes = map(int, text.split(":"))
    return hours + minutes / 60


def parse_eva(raw: dict) -> Eva | None:
    """Return None if the record has no usable duration."""
    duration = raw.get("duration")
    if not duration:
        return None
    try:
        hours = parse_duration(duration)
    except ValueError:
        return None

    date = raw.get("date")
    return Eva(
        country=raw.get("country") or None,
        date=datetime.fromisoformat(date) if date else None,
        duration_hours=hours,
    )


def parse_evas(records: list[dict]) -> list[Eva]:
    return [eva for eva in map(parse_eva, records) if eva is not None]
