import json
from pathlib import Path

from .models import Eva
from .parsing import parse_evas


def load_evas(path: str | Path) -> list[Eva]:
    with open(path, "r", encoding="utf-8") as file:
        return parse_evas(json.load(file))
