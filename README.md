# Data Cleaning Utils

Dependency-free Python helpers I use for preparing small annotation and evaluation datasets. The functions favor predictable behavior and readable code over a large framework.

## Included helpers

- `clean_csv()` normalizes selected text columns and removes duplicate records.
- `remove_duplicates()` preserves the first occurrence while keeping input order.
- `fix_json()` removes null items from JSON lists and can write formatted output.
- `normalize_text()` trims, collapses whitespace, and applies case folding.

## Before and after

`sample.csv` starts with inconsistent casing, extra spaces, and a repeated row:

```text
id,label,comment
1, Positive,  Clear answer
2,negative,Needs review
2,negative,Needs review
```

```python
from cleaner import clean_csv
clean_csv("sample.csv", "cleaned.csv", text_fields=("label", "comment"))
```

The cleaned output has one copy of row 2 and normalized text:

```text
id,label,comment
1,positive,clear answer
2,negative,needs review
```

`sample.json` contains a `null` item. `fix_json("sample.json", "fixed.json")` keeps the useful objects and writes readable, indented JSON.

## Run a quick check

```bash
python -m py_compile cleaner.py
```

## Tech stack

Python 3.9+ and the standard library.
