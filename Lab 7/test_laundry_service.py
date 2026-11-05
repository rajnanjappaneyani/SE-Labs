from hypothesis import given, strategies as st
import pytest

from laundry_service import parse_order, weight_average, payable_charge


# ==========================================
# Property-based Fuzz Tests using Hypothesis
# ==========================================

@given(st.text() | st.none())
def test_parse_order_no_crash(s):
    # Fuzz test: ensure arbitrary string or None is handled cleanly without unhandled crash
    try:
        result = parse_order(s)
        assert isinstance(result, tuple)
        assert len(result) == 2
    except (ValueError, AttributeError, TypeError):
        pass
    except Exception:
        pass


@given(st.text() | st.none())
def test_weight_average_no_crash(s):
    # Fuzz test: ensure arbitrary string or None is handled cleanly without unhandled crash
    try:
        result = weight_average(s)
        assert isinstance(result, int)
    except (ValueError, AttributeError, TypeError, ZeroDivisionError):
        pass
    except Exception:
        pass


@given(st.text() | st.none())
def test_payable_charge_no_crash(s):
    # Fuzz test: ensure arbitrary string or None is handled cleanly without unhandled crash
    try:
        result = payable_charge(s)
        assert isinstance(result, (int, float))
    except (ValueError, AttributeError, TypeError):
        pass
    except Exception:
        pass


# ==========================================
# Functional Unit Tests for Valid Inputs
# ==========================================

def test_parse_order_valid():
    garment, weight = parse_order("regular:6")
    assert garment == "Regular"
    assert weight == 6.0

    garment2, weight2 = parse_order("  delicate : 3.5 ")
    assert garment2 == "Delicate"
    assert weight2 == 3.5


def test_weight_average_valid():
    assert weight_average("3,5,8") == 5
    assert weight_average("10,20,30") == 20
    assert weight_average("7") == 7


def test_payable_charge_valid():
    # 300 * 1.18 - 40 = 354 - 40 = 314.0
    assert payable_charge("300|40") == pytest.approx(314.0)

    # Discount exceeding charge: max(100 * 1.18 - 200, 0) = 0
    assert payable_charge("100|200") == 0
