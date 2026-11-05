# Lab 5: Static Code Analysis — Library Catalog System

Static code analysis and remediation of the Library Catalog System using **Pylint**, **Bandit**, and **Flake8**.

## Files

| File | Description |
|------|-------------|
| `library_catalog_system.py` | Refactored and cleaned library catalog manager (Pylint 10.00/10, 0 Bandit issues, 0 Flake8 violations). |
| `issues.md` | Issue log detailing identified vulnerabilities, code defects, descriptions, and fix strategies. |
| `reflection.md` | Responses to the four static analysis reflection prompts. |
| `pylint_report.txt` / `pylint_after.txt` | Clean Pylint verification report (10.00/10). |
| `bandit_report.txt` / `bandit_after.txt` | Clean Bandit security report (0 issues). |
| `flake8_report.txt` / `flake8_after.txt` | Clean Flake8 style report (0 violations). |
| `pylint_before.txt` | Baseline Pylint report before fixes (5.11/10). |
| `bandit_before.txt` | Baseline Bandit report before fixes (5 issues). |
| `flake8_before.txt` | Baseline Flake8 report before fixes (6 violations). |

## Running the Analysis

```bash
# Run the cleaned program
python library_catalog_system.py

# Run static code analyzers
pylint library_catalog_system.py
bandit -r library_catalog_system.py
flake8 library_catalog_system.py
```
