import pytest

from laundry_service import (
    dropoff_status,
    extra_weight_charge,
    order_acceptable,
)


@pytest.mark.parametrize(
    ("garment", "weight", "speed", "member", "expected"),
    [
        ("regular", 4, "standard", False, 0),
        ("regular", 7, "standard", False, 60),
        ("regular", 7, "express", False, 100),
        ("delicate", 6, "standard", True, 30),
        ("bedding", 9, "standard", True, 50),
        ("regular", 16, "standard", False, 495),
        ("regular", 16, "express", False, 825),
    ],
)
def test_extra_weight_charge(garment, weight, speed, member, expected):
    assert extra_weight_charge(garment, weight, speed, member) == expected


def test_unknown_garment_is_rejected():
    with pytest.raises(ValueError, match="unknown garment type"):
        extra_weight_charge("shoes", 4, "standard", False)


def test_negative_weight_is_rejected():
    with pytest.raises(ValueError, match="invalid weight"):
        extra_weight_charge("regular", -1, "standard", False)


@pytest.mark.parametrize(
    ("weight", "items", "delicate", "expected"),
    [
        (10, 20, False, True),
        (26, 20, False, False),
        (10, 41, False, False),
        (10, 5, True, True),
        (30, 6, True, False),
    ],
)
def test_order_acceptable(weight, items, delicate, expected):
    assert order_acceptable(weight, items, delicate) is expected


@pytest.mark.parametrize(
    ("minutes", "bedding", "express", "expected"),
    [
        (60, False, False, "accepted"),
        (45, False, False, "late"),
        (39, False, False, "rejected"),
        (90, True, False, "accepted"),
        (75, True, False, "late"),
        (120, True, True, "accepted"),
        (105, True, True, "late"),
        (89, True, True, "rejected"),
    ],
)
def test_dropoff_status(minutes, bedding, express, expected):
    assert dropoff_status(minutes, bedding, express) == expected
