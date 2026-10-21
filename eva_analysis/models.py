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


@dataclass(frozen=True)
class CountrySummary:
    country: str
    eva_count: int
    total_hours: float

    @property
    def average_hours(self) -> float | None:
        return self.total_hours / self.eva_count if self.eva_count else None
