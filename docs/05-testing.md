# Evaluation

## Architectural Evaluation

Only 4 modules needed modification, and all the changes were added behaviour.
Existing behaviour was not modified.

The module dependency tree can be viewed in 02a-proposed-architecture.png.

Calculations can be tested with no I/O

Responsibilities are much easier to identify, both through module naming and
at a glance through the modules.

Duplication has been reduced, as dependencies and helpers can be used instead of
rewriting the functionality.

Care was taken to avoid introducing unnecessary complexity. For example, multiple
input file types are not supported - only JSON. However, it could be argued that some of
the modules could be combined to make them smaller. I do not believe this is necessary,
as these new modules would be difficult to name or label with a single responsibility,
which is indicative of overloaded concerns.

This also applies to tests. Certain functionality was not tested, for example, the CLI.
This is because the goal of a CLI is to be a thin wrapper over business logic, so it should
itself not be complex enough to require testing. Testing this would not provide utility and
would introduce complexity.

## Test Evidence

```
❯ uv run pytest                                                                    20:59
================================== test session starts ==================================
platform darwin -- Python 3.14.8, pytest-9.1.1, pluggy-1.7.0
rootdir: /Users/fred/Code/College/Topics/Architecture/Developers/Naem/Software-Architecture-Weekly
configfile: pyproject.toml
testpaths: tests
collected 42 items

tests/test_analysis.py ......................                                     [ 52%]
tests/test_io.py ...                                                              [ 59%]
tests/test_parsing.py ............                                                [ 88%]
tests/test_reporting.py .....                                                     [100%]

================================== 42 passed in 0.23s ===================================
```
