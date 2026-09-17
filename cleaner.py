"""Practical, dependency-free helpers for small annotation datasets."""

import csv
import json
import re
from pathlib import Path
from typing import Any, Iterable


def normalize_text(value: str) -> str:
    """Trim whitespace, collapse repeated spaces, and normalize casing."""
    value = re.sub(r"\s+", " ", str(value)).strip()
    return value.casefold()


def remove_duplicates(rows: Iterable[dict], key_fields: tuple[str, ...] | None = None) -> list[dict]:
    """Keep the first occurrence of each row or key, preserving input order."""
    seen = set()
    result = []
    for row in rows:
        key = tuple(row.get(field) for field in key_fields) if key_fields else tuple(sorted(row.items()))
        if key not in seen:
            seen.add(key)
            result.append(row)
    return result


def clean_csv(input_path: str, output_path: str, text_fields: tuple[str, ...] = ()) -> int:
    """Normalize selected fields and remove duplicate records from a CSV file."""
    with Path(input_path).open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    cleaned = []
    for row in remove_duplicates(rows):
        for field in text_fields:
            if field in row:
                row[field] = normalize_text(row[field])
        cleaned.append(row)

    with Path(output_path).open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned)
    return len(cleaned)


def fix_json(input_path: str, output_path: str | None = None) -> Any:
    """Load JSON, remove null-only records, and optionally write pretty JSON."""
    with Path(input_path).open(encoding="utf-8") as source:
        data = json.load(source)
    if isinstance(data, list):
        data = [item for item in data if item is not None]
    if output_path:
        with Path(output_path).open("w", encoding="utf-8") as target:
            json.dump(data, target, indent=2, ensure_ascii=False)
            target.write("\n")
    return data
