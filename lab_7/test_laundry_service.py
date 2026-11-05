from hypothesis import given, strategies as st
import pytest

from laundry_service import parse_order, payable_charge, weight_average


@given(st.text())
def test_parse_order_arbitrary_text_is_valid_or_rejected_cleanly(text):
    try:
        garment, kg = parse_order(text)
    except ValueError:
        return
    assert garment
    assert kg >= 0


@given(st.lists(st.integers(min_value=0, max_value=100_000), min_size=1, max_size=30))
def test_weight_average_matches_integer_average(values):
    csv = ",".join(map(str, values))
    assert weight_average(csv) == sum(values) // len(values)


@given(st.text())
def test_weight_average_arbitrary_text_is_valid_or_rejected_cleanly(text):
    try:
        result = weight_average(text)
    except ValueError:
        return
    assert isinstance(result, int)


@given(st.tuples(st.floats(min_value=0, max_value=1_000_000, allow_nan=False, allow_infinity=False),
                 st.floats(min_value=0, max_value=1_000_000, allow_nan=False, allow_infinity=False)))
def test_payable_charge_is_nonnegative(charge_discount):
    charge, discount = charge_discount
    result = payable_charge(f"{charge}|{discount}")
    assert result == max(charge * 1.18 - discount, 0)


@given(st.text())
def test_payable_charge_arbitrary_text_is_valid_or_rejected_cleanly(text):
    try:
        result = payable_charge(text)
    except ValueError:
        return
    assert result >= 0
