# Architectural Decision Record

## ADR-001: Let I/O-based Code Depend on Pure Logic

### Context

The original script mixes input(), print(), JSON loading, business rules, CSV writing, and plotting in one scope. Consequences:

Nothing can be tested without running the whole script and typing a country.
A change to one concern (e.g. the output format) risks breaking another (e.g. the duration thresholds).
exit() and plt.show() make the script awkward to reuse, automate, or run headless.

### Alternatives Considered

1. Keep as a single script, add comments. Low effort, does not fix problem structurally.
2. Class-based design. Groups related behaviour, but risks re-coupling logic.
3. Layered modules with IO modules depending on pure modules.

### Decision Taken

Split the code into separate modules based on _purity_. Code that uses I/O should
depend on pure modules and functions, never the other way around. User interaction
should be at the highest level of the dependency tree.

### Rationale

Testability is the feature most lacking from the project at present. The best way to
fix this is to split the code into functions that can be called without I/O.
Grouping these functions by module makes the code more readable and easy to update.

### Consequences

The code should be more readable, testable, and extensible. Testability is likely
the largest benefit - currently, when conducting this refactoring, I will have to rely on
golden tests to ensure the functionality is unchanged from the original code

Navigation overhead is introduced due to the many files for such a small project.

## ADR-002: Parse raw records into typed domain objects once, at the boundary

The script works directly on raw JSON dicts. Every use site must re-check for missing or
empty fields (if not duration_text, if country and ..., if not date_text) and re-derive
values such as hours from "H:MM" strings. Validation is scattered, and a malformed duration
crashes the script with an unhandled ValueError mid-run.

### Alternatives

1. Keep as-is, add more defensive checks.
2. Use a dataframe library, such as pandas.
3. Use a model class that is created once when loading data.

### Decision

Go with option 3. A model is almost always best practice in a case such as this. It
makes expected values and types explicit, introduces an ergonomic API for users,
and prevents the need for repeated checks.

### Consequences

- Benefits: downstream functions are simpler, parse_duration is testable in isolation, and the data contract is documented in one class.
- Limitations: returning None silently drops bad records, which hides data-quality problems.
Could replace with other functionality in the future.
- Trade-offs: an extra translation layer and one more type to maintain, in exchange for localized, explicit validation. Switching to pandas later would mean replacing `analysis.py` but not the boundary concept.

## ADR-003: Replace the fused loop with independent single-purpose analysis functions

### Context

One loop computes three unrelated results: the selected country's total hours, the duration-category counts, and the cumulative time series. Each has different filtering rules, and the fused loop hides this. For example, a record with a duration but no date counts toward the category tallies and the country total, but is silently excluded from the time series. This looks accidental. The loop also cannot be tested per result, and changing one calculation risks side effects on the others.

### Alternatives

1. Keep the single loop, add comments documenting filter rules. It preserves single-pass efficiency, but the coupling remains.
2. A single `compute_all()` function returning a results object. It centralizes the logic but is still one function with three responsibilities.
3. One pure function per question (`total_hours_for_country`, `category_counts`, `cumulative_series`), each with its own explicit filter, called separately by the orchestrator.

### Decision

Adopt option 3. Each function takes a `list[Eva]` and returns one result. Thresholds are named constants (`SHORT_LIMIT_HOURS = 4`, `STANDARD_LIMIT_HOURS = 7`). The existing filtering behavior is deliberately preserved, and the decision is recorded: `parse_eva` keeps undated records, and `cumulative_series` is the one function that filters them out.

### Rationale

- Each function has one reason to change and one filter rule that can be read, tested, and debated in isolation.
- Prefer clarity over efficiency

Consequences

- _Benefits:_ boundary tests are easy (exactly 4.0 and 7.0 hours), new metrics can be added without touching existing ones, and the semantics are explicit.
- _Limitations:_ the data is traversed three times instead of once, which could matter on very large datasets.
- _Trade-offs:_ a bit more code and more public functions in exchange for clarity and independent testability
