from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class DurationCategory(Enum):
    SHORT = "Short"
    STANDARD = "Standard"
    LONG = "Long"


@dataclass(frozen=True)
class Eva:
    country: str | None
    date: datetime | None
    duration_hours: float
