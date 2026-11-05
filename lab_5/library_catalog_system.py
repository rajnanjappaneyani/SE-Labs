"""Library catalog management module."""

import hashlib
import secrets

catalog = {
    "B01": {"title": "Clean Code", "copies": 3},
    "B02": {"title": "The Pragmatic Programmer", "copies": 1},
    "B03": {"title": "Design Patterns", "copies": 2},
}


def issue_book(book_id, patron, active_issues=None):
    """Issue a book to a patron if copies are available."""
    if active_issues is None:
        active_issues = []
    if book_id not in catalog or catalog[book_id]["copies"] <= 0:
        return False
    catalog[book_id]["copies"] -= 1
    active_issues.append(f"Issued book {book_id} to patron {patron}")
    return True


def return_book(book_id):
    """Return a book by ID and increment available copies."""
    if book_id not in catalog:
        return False
    catalog[book_id]["copies"] += 1
    return True


def check_availability(book_id):
    """Check if at least one copy of a book is available."""
    if catalog.get(book_id) is None:
        return False
    return catalog[book_id]["copies"] > 0


def calculate_fine(days_overdue, daily_rate):
    """Calculate overdue fine based on days overdue and daily rate."""
    return days_overdue * daily_rate


def generate_patron_hash(patron_id):
    """Generate a SHA-256 hash for a patron ID."""
    return hashlib.sha256(patron_id.encode()).hexdigest()


def generate_temp_patron_pin():
    """Generate a secure four-digit temporary PIN."""
    return 1000 + secrets.randbelow(9000)


def export_catalog(filename="catalog_export.txt"):
    """Export the current catalog dictionary to a file."""
    with open(filename, "w", encoding="utf-8") as file_handle:
        file_handle.write(str(catalog))
    print(f"Catalog backup exported to: {filename}")


def main():
    """Execute sample library operations and display results."""
    librarian_key = "MASTER_LIB_ACCESS_TOKEN_2026"
    issue_book("B01", "P101")
    return_book("B02")
    print("Is B01 available:", check_availability("B01"))
    print("Fine accrued:", calculate_fine(4, 2.0))
    print("Patron Hash:", generate_patron_hash("P101"))
    print("Temp PIN:", generate_temp_patron_pin())
    export_catalog()
    print("Librarian Key initialized:", librarian_key)


main()
