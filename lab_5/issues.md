# Lab 5: Static Code Analysis — Issue Log

**File analyzed:** `library_catalog_system.py`  
**Tools used:** Pylint, Bandit, Flake8

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command execution (B605) | Security - High | 58 | `os.system()` executes an echo command via a subshell with string concatenation, exposing potential command injection risks. | Replaced `os.system` with a native, safe Python `print()` statement and removed `import os`. |
| Weak MD5 hash (B324) | Security - High | 47 | Insecure MD5 hashing algorithm used for sensitive patron identifier hashing. | Upgraded hash algorithm to cryptographically secure SHA-256 (`hashlib.sha256()`). |
| Arbitrary code execution via `eval` (B307) | Security - Medium | 42 | Using `eval()` on unvalidated dynamic expression strings allows arbitrary Python code execution. | Replaced `eval()` with explicit arithmetic multiplication `days_overdue * daily_rate`. |
| Insecure pseudo-random generator (B311) | Security - Low | 50–51 | `random.randint()` is not cryptographically secure for generating sensitive authentication tokens/PINs. | Replaced `random` with the cryptographically secure `secrets` module (`secrets.randbelow()`). |
| Bare exception / try-except-pass (B110, E722, W0702) | Security & Quality - Low | 23–27 | A bare `except:` block silently suppresses all exceptions, masking potential runtime errors and key errors. | Handled invalid `book_id` explicitly with a membership check (`if book_id not in catalog: return False`). |
| Mutable default argument (W0102) | Bug Risk | 15 | `active_issues=[]` uses a mutable list default, which persists mutations across subsequent function invocations. | Changed the default value to `None` and initialized a new list instance when `None`. |
| Unused import (F401, W0611) | Style & Cleanliness | 6 | `csv` was imported but never utilized anywhere in the code. | Removed the unused `import csv` statement. |
| Unused local variables (F841, W0612) | Quality & Style | 31, 41 | Variables `late_fee` and `days` were assigned values but never read. | Removed unnecessary variable assignments. |
| Non-idiomatic None comparison (E711, C0121) | Style | 32 | Used equality operator `catalog.get(book_id) == None` instead of identity comparison `is None`. | Changed the expression to `catalog.get(book_id) is None`. |
| Insecure / unmanaged file I/O (R1732, W1514) | Resource Management | 55–57 | File opened with raw `open()`, unmanaged without a context manager and without specifying text encoding. | Used a `with open(..., encoding="utf-8")` context manager for safe and deterministic resource cleanup. |
| Function naming convention (C0103) | Style | 15 | Function `issueBook` used camelCase instead of PEP 8 standard snake_case. | Renamed function to `issue_book` and updated call sites accordingly. |
| Missing docstrings (C0116) | Maintainability | 15, 23, 30, 40, 46, 50, 54, 61 | Functions lacked descriptive docstrings explaining their parameters, behavior, and return values. | Added PEP 257 compliant docstrings to all functions. |
| Missing trailing newline (W292, C0304) | Style | 73 | The source file lacked a terminating newline character. | Added a trailing newline to the end of the file. |

---

## Verification Results

### Before Fixes
- **Pylint score:** 5.11 / 10
- **Bandit issues:** 5 findings (2 High, 1 Medium, 2 Low)
- **Flake8 violations:** 6 violations (F401, E722, F841, E711, F841, W292)

### After Fixes
- **Pylint score:** **10.00 / 10**
- **Bandit issues:** **0 issues identified**
- **Flake8 violations:** **0 violations reported**
