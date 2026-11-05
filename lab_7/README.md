# Lab 7 — Fuzz Testing

Uses Hypothesis to generate valid and arbitrary inputs for laundry order parsing, weight averaging, and payable charge calculations. Invalid inputs are rejected with `ValueError`; generated valid inputs are checked against their expected properties.

## Files

- `laundry_service.py` — validated service functions and interactive entry point.
- `test_laundry_service.py` — property-based and arbitrary-text fuzz tests.
- `requirements.txt` — test dependencies.

## Run

From this folder, install dependencies with `pip install -r requirements.txt`, then run `pytest`.
