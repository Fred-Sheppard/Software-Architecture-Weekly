# Software-Architecture-Weekly

## Structure

The analysis lives in the `eva_analysis` package. Pure logic is separated from
side effects, and dependencies point inward towards the domain model:

| Module | Responsibility |
| --- | --- |
| `models.py` | `Eva` dataclass and `DurationCategory` enum |
| `parsing.py` | Raw JSON record to `Eva`, `"H:MM"` to hours |
| `analysis.py` | Country totals, duration categories, cumulative series |
| `repository.py` | Loading EVAs from the JSON file |
| `reporting.py` | Text report and CSV output |
| `plotting.py` | Cumulative duration chart |
| `cli.py` | Argument parsing, prompting, and orchestration |

Records without a usable duration (missing or malformed) are dropped during
parsing. As described above, undated records still count towards the country
total and duration categories but are excluded from the cumulative plot. Each
rule now lives in its own function in `analysis.py`.

## Assessment

The evaluation and documentation can be found in `docs/`.

## Usage

This project can be run using `uv`.

```sh
uv run python -m eva_analysis                      # prompts for a country
uv run python -m eva_analysis --country USA --no-show
uv run python -m eva_analysis --help
uv run python -m eva_analysis compare              # prompts for countries and years
uv run python -m eva_analysis compare --country-a USA --country-b Russia --start-year 1990 --end-year 2000
```

## Tests

```sh
uv run pytest
```
