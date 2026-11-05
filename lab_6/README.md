# Lab 6 — Code and Branch Coverage

Tests the laundry service's extra-weight pricing, order acceptance rules, and drop-off cutoff statuses.

## Files

- `laundry_service.py` — supplied service logic.
- `test_laundry_service.py` — parameterized coverage tests, including validation failures and decision branches.

## Run

From this folder, install `pytest` and `pytest-cov`, then run `pytest --cov=laundry_service --cov-branch --cov-report=term-missing`. The tests target high statement and branch coverage for the supplied module.
