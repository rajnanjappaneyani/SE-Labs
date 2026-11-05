import math


def parse_order(text):
    """Parse a garment and weight written as ``garment:kg``."""
    if not isinstance(text, str):
        raise ValueError("order must be text")
    parts = text.split(":")
    if len(parts) != 2 or not parts[0].strip():
        raise ValueError("order must have garment:weight format")
    try:
        kg = float(parts[1].strip())
    except ValueError as exc:
        raise ValueError("weight must be numeric") from exc
    if not math.isfinite(kg) or kg < 0:
        raise ValueError("weight must be finite and nonnegative")
    return parts[0].strip().title(), kg


def weight_average(weights_csv):
    """Return the integer average of comma-separated nonnegative weights."""
    if not isinstance(weights_csv, str):
        raise ValueError("weights must be text")
    parts = weights_csv.split(",")
    if not parts or any(not part.strip() for part in parts):
        raise ValueError("weights must be a non-empty comma-separated list")
    try:
        values = [int(part.strip()) for part in parts]
    except ValueError as exc:
        raise ValueError("weights must be integers") from exc
    if any(value < 0 for value in values):
        raise ValueError("weights cannot be negative")
    return sum(values) // len(values)


def payable_charge(text):
    """Calculate an 18% tax-inclusive charge less a discount, floored at zero."""
    if not isinstance(text, str):
        raise ValueError("charge must be text")
    parts = text.split("|")
    if len(parts) != 2:
        raise ValueError("charge must have charge|discount format")
    try:
        charge, discount = (float(part.strip()) for part in parts)
    except ValueError as exc:
        raise ValueError("charge and discount must be numeric") from exc
    if not math.isfinite(charge) or not math.isfinite(discount) or charge < 0 or discount < 0:
        raise ValueError("charge and discount must be finite and nonnegative")
    total = charge * 1.18 - discount
    return max(total, 0)


def main():
    print("==== Running parse_order ====")
    result = parse_order(input("Enter garment:weight in kg (e.g. regular:6): "))
    print("Garment and Weight:", result)

    print("\n==== Running weight_average ====")
    result = weight_average(input("Enter garment weights as CSV (e.g. 3,5,8): "))
    print("Average Weight:", result)

    print("\n==== Running payable_charge ====")
    result = payable_charge(input("Enter charge|discount (e.g. 300|40): "))
    print("Payable Charge:", result)


if __name__ == "__main__":
    main()
